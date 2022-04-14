#!/usr/bin/env -S scala-cli shebang --scala-version 3.1.1

/*
Brian Schlining
Copyright 2022, Monterey Bay Aquarium Research Institute
*/

//> using lib "org.apache.derby:derby:10.15.2.0"
//> using lib "org.apache.derby:derbyclient:10.15.2.0"
//> using lib "org.apache.derby:derbynet:10.15.2.0"
//> using lib "org.apache.derby:derbyshared:10.15.2.0"
//> using lib "com.microsoft.sqlserver:mssql-jdbc:9.4.1.jre11"
//> using lib "com.oracle.ojdbc:ojdbc8:19.3.0.0"
//> using lib "org.jasypt:jasypt:1.9.3"
//> using lib "org.postgresql:postgresql:42.3.3"

import java.sql.DriverManager
import java.sql.ResultSet
import java.sql.Connection

case class TableCol[T](name: String, fn: ResultSet => T)
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
  while(rows.next) {
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
    println(sqlInsert)
    destStmt.executeUpdate(sqlInsert)
  }
  dest.commit() 
  srcStmt.close()
  destStmt.close()  
}

def copyImagedMoments(src: Connection, dest: Connection): Unit = {
  println("Copying imaged_moments")
  val srcs = TableSrc("IMAGED_MOMENTS",
    Seq(
      TableCol("UUID", rs => rs.getObject("UUID").toString.toLowerCase),
      TableCol("ELAPSED_TIME_MILLIS", rs => rs.getLong("ELAPSED_TIME_MILLIS")),
      TableCol("LAST_UPDATED_TIMESTAMP", rs => rs.getTimestamp("LAST_UPDATED_TIME")),
      TableCol("RECORDED_TIMESTAMP", rs => rs.getTimestamp("RECORDED_TIMESTAMP")),
      TableCol("TIMECODE", rs => rs.getString("TIMECODE")),
      TableCol("VIDEO_REFERENCE_UUID", rs => rs.getObject("VIDEO_REFERENCE_UUID").toString.toLowerCase),
    )
  )
  copy(srcs, src, dest)
}

def copyImageReferences(src: Connection, dest: Connection): Unit = {
  println("Copying image_references")
  val srcs = TableSrc("IMAGE_REFERENCES", 
    Seq(
      TableCol("UUID", rs => rs.getObject("UUID").toString.toLowerCase),
      TableCol("DESCRIPTION", rs => rs.getString("DESCRIPTION")),
      TableCol("FORMAT", rs => rs.getString("FORMAT")),
      TableCol("HEIGHT_PIXELS", rs => rs.getInt("HEIGHT_PIXELS")),
      TableCol("LAST_UPDATED_TIMESTAMP", rs.getTimestamp("LAST_UPDATED_TIMESTAMP")),
      TableCol("URL", rs => rs.getString("URL")),
      TableCol("WIDTH_PIXELS", rs => rs.getInt("WIDTH_PIXELS")),
      TableCol("IMAGED_MOMENT_UUID", rs => rs.getObject("IMAGED_MOMENT_UUID").toString.toLowerCase)
    )
  )
  copy(srcs, src, dest)
}


def copyAncillaryData(src: Connection, dest: Connection): Unit = {
  println("Copying ancillary_data")
  val srcs = TableSrc("ANCILLARY_DATA", 
    Seq(
      TableCol("UUID", rs => rs.getObject("UUID").toString.toLowerCase),
      TableCol("ALTITUDE", rs => rs.getDouble("ALTITUDE")),
      TableCol("COORDINATE_REFERENCE_SYSTEM", rs => rs.getString("COORDINATE_REFERENCE_SYSTEM")),
      TableCol("LAST_UPDATED_TIMESTAMP", rs.getTimestamp("LAST_UPDATED_TIMESTAMP")),
      TableCol("DEPTH_METERS", rs => rs.getDouble("DEPTH_METERS")),
      TableCol("LATITUDE", rs => rs.getDouble("LATITUDE")),
      TableCol("LONGITUDE", rs => rs.getDouble("LONGITUDE")),
      TableCol("OXYGEN_ML_PER_L", rs => rs.getDouble("OXYGEN_ML_PER_L")),
      TableCol("PHI", rs => rs.getDouble("phi")),
      TableCol("XYZ_POSITION_UNITS", rs => rs.getString("XYZ_POSITION_UNITS")),
      TableCol("PRESSURE_DBAR", rs => rs.getDouble("PRESSURE_DBAR")),
      TableCol("PSI", rs => rs.getDouble("psi")),
      TableCol("SALINITY", rs => rs.getDouble("SALINITY")),
      TableCol("TEMPERATURE_CELSIUS", rs => rs.getDouble("TEMPERATURE_CELSIUS")),
      TableCol("THETA", rs => rs.getDouble("theta")),
      TableCol("X", rs => rs.getDouble("X")),
      TableCol("Y", rs => rs.getDouble("Y")),
      TableCol("Z", rs => rs.getDouble("Z")),
      TableCol("IMAGED_MOMENT_UUID", rs => rs.getObject("IMAGED_MOMENT_UUID").toString.toLowerCase),
      TableCol("LIGHT_TRANSMISSION", rs => rs.getDouble("LIGHT_TRANSMISSION"))
    )
  )
  copy(srcs, src, dest)
}

def copyObservations(src: Connection, dest: Connection): Unit = {
  println("Copying observations")
  val srcs = TableSrc("OBSERVATIONS", 
    Seq(
      TableCol("UUID", rs => rs.getObject("UUID").toString.toLowerCase),
      TableCol("ACTIVITY", rs => rs.getString("ACTIVITY")),
      TableCol("CONCEPT", rs => rs.getString("CONCEPT")),
      TableCol("DURATION_MILLIS", rs => rs.getLong("DURATION_MILLIS")),
      TableCol("OBSERVATION_GROUP", rs => rs.getString("OBSERVATION_GROUP")),
      TableCol("LAST_UPDATED_TIMESTAMP", rs.getTimestamp("LAST_UPDATED_TIMESTAMP")),
      TableCol("OBSERVATION_TIMESTAMP", rs => rs.getTimestamp("OBSERVATION_TIMESTAMP")),
      TableCol("OBSERVER", rs => rs.getString("OBSERVER")),
      TableCol("IMAGED_MOMENT_UUID", rs => rs.getObject("IMAGED_MOMENT_UUID").toString.toLowerCase)
    )
  )
  copy(srcs, src, dest)
}

def copyAssociations(src: Connection, dest: Connection): Unit = {
  println("Copying associations")
  val srcs = TableSrc("ASSOCIATIONS", 
    Seq(
      TableCol("UUID", rs => rs.getObject("UUID").toString.toLowerCase),
      TableCol("LAST_UPDATED_TIMESTAMP", rs.getTimestamp("LAST_UPDATED_TIMESTAMP")),
      TableCol("LINK_NAME", rs => rs.getString("LINK_NAME")),
      TableCol("LINK_VALUE", rs => rs.getString("LINK_VALUE")),
      TableCol("TO_CONCEPT", rs => rs.getString("TO_CONCEPT")),
      TableCol("OBSERVATION_UUID", rs => rs.getObject("OBSERVATION_UUID").toString.toLowerCase),
      TableCol("MIME_TYPE", rs => rs.getString("MIME_TYPE")),
    )
  )
  copy(srcs, src, dest)
}

def copyVideoReferenceInformation(src: Connection, dest: Connection): Unit = {
  println("Copying video_reference_information")
  val srcs = TableSrc("VIDEO_REFERENCE_INFORMATION", 
    Seq(
      TableCol("UUID", rs => rs.getObject("UUID").toString.toLowerCase),
      TableCol("LAST_UPDATED_TIMESTAMP", rs.getTimestamp("LAST_UPDATED_TIMESTAMP")),
      TableCol("MISSION_CONTACT", rs => rs.getString("MISSION_CONTACT")),
      TableCol("MISSION_ID", rs => rs.getString("MISSION_ID")),
      TableCol("PLATFORM_NAME", rs => rs.getString("PLATFORM_NAME")),
      TableCol("VIDEO_REFERENCE_UUID", rs => rs.getObject("VIDEO_REFERENCE_UUID").toString.toLowerCase)
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
