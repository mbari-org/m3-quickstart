#!/usr/bin/env -S scala-cli shebang

/*
bin/vars_migrate_vampiresquid.sh "jdbc:derby://localhost:1527/M3_ANNOTATIONS" varsuser "jdbc:postgresql://localhost:5432/M3_VARS?sslmode=disable&stringType=unspecified" m3

Brian Schlining
Copyright 2022, Monterey Bay Aquarium Research Institute
*/



import java.sql.DriverManager
import java.sql.ResultSet
import java.sql.Connection

trait TableCol[T] {
  def name: String
  def fn: ResultSet => T
}

final case class StringCol(name: String) extends TableCol[String] {
  val fn: ResultSet => String = rs => {
    Option(rs.getObject(name)) match {
      case None => "NULL"
      case Some(v) => s"'${v.toString.replace("'", "''")}'"
    }
  }
}

final case class ObjectCol[T](name: String, fn: ResultSet => T) extends TableCol[T]

case class TableSrc(table: String, cols: Seq[TableCol[_]], orderCol: Option[String] = None)

def copy(tableSrc: TableSrc, src: Connection, dest: Connection): Unit = {
  val columns = tableSrc.cols.map(_.name).mkString(", ")
  val srcStmt = src.createStatement
  dest.setAutoCommit(false)
  val destStmt = dest.createStatement
  val sqlSelect = s"""
  |SELECT
  |  $columns
  |FROM
  |  ${tableSrc.table}
  |${tableSrc.orderCol.map(col => s"ORDER BY $col").getOrElse("")}
  |""".stripMargin
  println(sqlSelect)
  val rows = srcStmt.executeQuery(sqlSelect)
  var n = 0
  while(rows.next) {
    n = n + 1
    val values = tableSrc.cols
      .map(_.fn(rows))
      .map(v => v match {
          case s: String => if (s.equalsIgnoreCase("'null'")) "NULL" else s
          case _ => v
        }
      )
    val sqlInsert = s"""
    |INSERT INTO ${tableSrc.table}
    |  ($columns)
    |VALUES
    |  (${values.map(v => s"${v}").mkString(", ")})
    |""".stripMargin
    // println(sqlInsert)
    destStmt.addBatch(sqlInsert)
    if (n % 200 == 0) {
      destStmt.executeBatch()
      println(s"$n rows inserted")
    }
    // destStmt.executeUpdate(sqlInsert)
  }
  destStmt.executeBatch()
  dest.commit() 
  srcStmt.close()
  destStmt.close()  
}

def copyImagedMoments(src: Connection, dest: Connection): Unit = {
  println("Copying imaged_moments")
  val srcs = TableSrc("imaged_moments",
    Seq(
      ObjectCol("uuid", rs => s"'${rs.getObject("uuid").toString.toLowerCase}'"),
      ObjectCol("elapsed_time_millis", _.getLong("elapsed_time_millis")),
      StringCol("last_updated_timestamp"),
      StringCol("recorded_timestamp"),
      StringCol("timecode"),
      ObjectCol("video_reference_uuid", rs => s"'${rs.getObject("video_reference_uuid").toString.toLowerCase}'"),
    )
  )
  copy(srcs, src, dest)
}

def copyImageReferences(src: Connection, dest: Connection): Unit = {
  println("Copying image_references")
  val srcs = TableSrc("image_references", 
    Seq(
      ObjectCol("uuid", rs => s"'${rs.getObject("uuid").toString.toLowerCase}'"),
      StringCol("description"),
      StringCol("format"),
      ObjectCol("height_pixels", _.getInt("height_pixels")),
      StringCol("last_updated_timestamp"),
      StringCol("url"),
      ObjectCol("width_pixels", _.getInt("width_pixels")),
      ObjectCol("imaged_moment_uuid", rs => s"'${rs.getObject("imaged_moment_uuid").toString.toLowerCase}'")
    )
  )
  copy(srcs, src, dest)
}


def copyAncillaryData(src: Connection, dest: Connection): Unit = {
  println("Copying ancillary_data")
  val srcs = TableSrc("ancillary_data", 
    Seq(
      ObjectCol("uuid", rs => s"'${rs.getObject("uuid").toString.toLowerCase}'"),
      ObjectCol("altitude", _.getDouble("altitude")),
      StringCol("coordinate_reference_system"),
      StringCol("last_updated_timestamp"),
      ObjectCol("depth_meters", _.getDouble("depth_meters")),
      ObjectCol("latitude", _.getDouble("latitude")),
      ObjectCol("longitude", _.getDouble("longitude")),
      ObjectCol("oxygen_ml_per_l", _.getDouble("oxygen_ml_per_l")),
      ObjectCol("phi", _.getDouble("phi")),
      StringCol("xyz_position_units"),
      ObjectCol("pressure_dbar", _.getDouble("pressure_dbar")),
      ObjectCol("psi", _.getDouble("psi")),
      ObjectCol("salinity", _.getDouble("salinity")),
      ObjectCol("temperature_celsius", _.getDouble("temperature_celsius")),
      ObjectCol("theta", _.getDouble("theta")),
      ObjectCol("x", _.getDouble("x")),
      ObjectCol("y", _.getDouble("y")),
      ObjectCol("z", _.getDouble("z")),
      ObjectCol("imaged_moment_uuid", rs => s"'${rs.getObject("imaged_moment_uuid").toString.toLowerCase}'"),
      ObjectCol("light_transmission", _.getDouble("light_transmission"))
    )
  )
  copy(srcs, src, dest)
}

def copyObservations(src: Connection, dest: Connection): Unit = {
  println("Copying observations")
  val srcs = TableSrc("observations", 
    Seq(
      ObjectCol("uuid", rs => s"'${rs.getObject("uuid").toString.toLowerCase}'"),
      StringCol("activity"),
      StringCol("concept"),
      ObjectCol("duration_millis", _.getLong("duration_millis")),
      StringCol("observation_group"),
      StringCol("last_updated_timestamp"),
      StringCol("observation_timestamp"),
      StringCol("observer"),
      ObjectCol("imaged_moment_uuid", rs => s"'${rs.getObject("imaged_moment_uuid").toString.toLowerCase}'")
    )
  )
  copy(srcs, src, dest)
}

def copyAssociations(src: Connection, dest: Connection): Unit = {
  println("Copying associations")
  val srcs = TableSrc("associations", 
    Seq(
      ObjectCol("uuid", rs => s"'${rs.getObject("uuid").toString.toLowerCase}'"),
      StringCol("last_updated_timestamp"),
      StringCol("link_name"),
      StringCol("link_value"),
      StringCol("to_concept"),
      ObjectCol("observation_uuid", rs => s"'${rs.getObject("observation_uuid").toString.toLowerCase}'"),
      StringCol("mime_type"),
    )
  )
  copy(srcs, src, dest)
}

def copyVideoReferenceInformation(src: Connection, dest: Connection): Unit = {
  println("Copying video_reference_information")
  val srcs = TableSrc("video_reference_information", 
    Seq(
      ObjectCol("uuid", rs => s"'${rs.getObject("uuid").toString.toLowerCase}'"),
      StringCol("last_updated_timestamp"),
      StringCol("mission_contact"),
      StringCol("mission_id"),
      StringCol("platform_name"),
      ObjectCol("video_reference_uuid", rs => s"'${rs.getObject("video_reference_uuid").toString.toLowerCase}'")
    )
  )
  copy(srcs, src, dest)
}

def run(srcDbUrl: String,
    srcDbUser: String,
    srcDbPwd: String,
    destDbUrl: String,
    destDbUser: String,
    destDbPwd: String): Unit = {

  val src = DriverManager.getConnection(srcDbUrl, srcDbUser, srcDbPwd)
  val dest = DriverManager.getConnection(destDbUrl, destDbUser, destDbPwd)
  copyImagedMoments(src, dest)
  copyImageReferences(src, dest)
  copyAncillaryData(src, dest)
  copyObservations(src, dest)
  copyAssociations(src, dest)
  copyVideoReferenceInformation(src, dest)
  src.close()
  dest.close()
}

if (args.length != 4) {
  println("""Migrate Annosaurus data to another database.
    | Usage:
    |    export SRC_PWD=<database password>
    |    export DEST_PWD=<database password>
    |    MigrateAnnosaurus.sc <srcDbUrl> <srcDbUser> <destDbUrl> <destDbUser>
    |
    | Environment variables:
    |    SRC_PWD - password for source database
    |    DEST_PWD - password for destination database
    |
    | Arguments:
    |    srcDbUrl - JDBC URL for source database
    |    srcDbUser - user for source database
    |    destDbUrl - JDBC URL for destination database
    |    destDbUser - user for destination databases
    |""".stripMargin)
  System.exit(1)
}
else {
  val srcPwd = System.getenv("SRC_PWD")
  val destPwd = System.getenv("DEST_PWD")
  if (srcPwd == null) {
    println("SRC_PWD environment variable must be set")
    System.exit(1)
  }
  if (destPwd == null) {
    println("DEST_PWD environment variable must be set")
    System.exit(1)
  }
  println(s"Migrating video info from ${args(0)} to ${args(2)}")
  run(args(0), args(1), srcPwd, args(2), args(3), destPwd)
}
