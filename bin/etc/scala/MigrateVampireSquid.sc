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

def copyVideoSequences(src: Connection, dest: Connection): Unit = {
  println("Copying video_sequences")
  val srcs = TableSrc("video_sequences", 
    Seq(
      ObjectCol("uuid", rs => s"'${rs.getObject("uuid").toString.toLowerCase}'"),
      ObjectCol("name", rs => s"'${rs.getString(2)}'"),
      StringCol("camera_id"),
      StringCol("description"),
      ObjectCol("last_updated_time", rs => s"'${rs.getTimestamp("last_updated_time")}'")
    ))
  copy(srcs, src, dest)   
}

def copyVideos(src: Connection, dest: Connection): Unit = {
  println("Copying videos")
  val srcs = TableSrc("videos", 
    Seq(
      ObjectCol("uuid", rs => s"'${rs.getObject("uuid").toString.toLowerCase}'"),
      ObjectCol("video_sequence_uuid", rs => s"'${rs.getObject("video_sequence_uuid").toString.toLowerCase}'"),
      ObjectCol("name", rs => s"'${rs.getString(3)}'"),
      ObjectCol("start_time", rs => s"'${rs.getTimestamp("start_time")}'"),
      ObjectCol("duration_millis", _.getLong("duration_millis")),
      StringCol("description"),
      ObjectCol("last_updated_time", rs => s"'${rs.getTimestamp("last_updated_time")}'")
    ))
  copy(srcs, src, dest)
}

def copyVideoReferences(src: Connection, dest: Connection): Unit = {
  println("Copying video_references")
  // UUID, AUDIO_CODEC, CONTAINER, DESCRIPTION, FRAME_RATE (double), HEIGHT(int), LAST_UPDATED_TIME,
  // SHA512, SIZE_BYTES(long), URI, VIDEO_CODEC, WIDTH(int), VIDEO_UUID
  val srcs = TableSrc("video_references", 
  Seq(
    ObjectCol("uuid", rs => s"'${rs.getObject("uuid").toString.toLowerCase}'"),
    ObjectCol("video_uuid", rs => s"'${rs.getObject("video_uuid").toString.toLowerCase}'"),
    StringCol("audio_codec"),
    StringCol("container"),
    StringCol("description"),
    ObjectCol("frame_rate", _.getDouble("frame_rate")),
    ObjectCol("height", _.getInt("height")),
    StringCol("sha512"),
    ObjectCol("size_bytes", _.getLong("size_bytes")),
    ObjectCol("uri", rs =>  s"'${rs.getString("uri").replace("'", "''")}'"),
    StringCol("video_codec"),
    ObjectCol("width", _.getInt("width")),
    ObjectCol("last_updated_time", rs => s"'${rs.getTimestamp("last_updated_time")}'")
  ), Some("uri"))
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
  copyVideoSequences(src, dest)
  copyVideos(src, dest)
  copyVideoReferences(src, dest)
  src.close()
  dest.close()
}

if (args.length != 4) {
  println("""Migrate Vampire-squid data to another database.
    | Usage:
    |    export SRC_PWD=<database password>
    |    export DEST_PWD=<database password>
    |    MigrateVampireSquid.sc <srcDbUrl> <srcDbUser> <destDbUrl> <destDbUser>
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
