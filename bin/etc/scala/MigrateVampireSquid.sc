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

def copyVideoSequences(src: Connection, dest: Connection): Unit = {
  println("Copying video_sequences")
  val srcs = TableSrc("VIDEO_SEQUENCES", 
    Seq(
      TableCol("UUID", rs => s"'${rs.getObject("UUID").toString.toLowerCase}'"),
      TableCol("\"NAME\"", rs => s"'${rs.getString(2)}'"),
      TableCol("CAMERA_ID", rs => s"'${rs.getString("CAMERA_ID")}'"),
      TableCol("DESCRIPTION", rs => s"'${rs.getString("DESCRIPTION")}'"),
      TableCol("LAST_UPDATED_TIME", rs => s"'${rs.getTimestamp("LAST_UPDATED_TIME")}'")
    ))
  copy(srcs, src, dest)   
}

def copyVideos(src: Connection, dest: Connection): Unit = {
  println("Copying videos")
  val srcs = TableSrc("VIDEOS", 
    Seq(
      TableCol("UUID", rs => s"'${rs.getObject("UUID").toString.toLowerCase}'"),
      TableCol("VIDEO_SEQUENCE_UUID", rs => s"'${rs.getObject("VIDEO_SEQUENCE_UUID").toString.toLowerCase}'"),
      TableCol("\"NAME\"", rs => s"'${rs.getString(3)}'"),
      TableCol("START_TIME", rs => s"'${rs.getTimestamp("START_TIME")}'"),
      TableCol("DURATION_MILLIS", _.getLong("DURATION_MILLIS")),
      TableCol("DESCRIPTION", rs => s"'${rs.getString("DESCRIPTION")}'"),
      TableCol("LAST_UPDATED_TIME", rs => s"'${rs.getTimestamp("LAST_UPDATED_TIME")}'")
    ))
  copy(srcs, src, dest)
}

def copyVideoReferences(src: Connection, dest: Connection): Unit = {
  println("Copying video_references")
  // UUID, AUDIO_CODEC, CONTAINER, DESCRIPTION, FRAME_RATE (double), HEIGHT(int), LAST_UPDATED_TIME,
  // SHA512, SIZE_BYTES(long), URI, VIDEO_CODEC, WIDTH(int), VIDEO_UUID
  val srcs = TableSrc("VIDEO_REFERENCES", 
  Seq(
    TableCol("UUID", rs => s"'${rs.getObject("UUID").toString.toLowerCase}'"),
    TableCol("AUDIO_CODEC", rs => s"'${rs.getString("AUDIO_CODEC")}'"),
    TableCol("CONTAINER", rs => s"'${rs.getString("CONTAINER")}'"),
    TableCol("DESCRIPTION", rs => s"'${rs.getString("DESCRIPTION")}'"),
    TableCol("FRAME_RATE", rs => rs.getDouble("FRAME_RATE")),
    TableCol("HEIGHT", rs => rs.getInt("HEIGHT")),
    TableCol("SHA512", rs => s"'${rs.getString("SHA512")}'"),
    TableCol("SIZE_BYTES", rs => rs.getLong("SIZE_BYTES")),
    TableCol("URI", rs =>  s"'${rs.getString("URI").replace("'", "''")}'"),
    TableCol("VIDEO_CODEC", rs => s"'${rs.getString("VIDEO_CODEC")}'"),
    TableCol("WIDTH", rs => rs.getInt("WIDTH")),
    TableCol("VIDEO_UUID", rs => s"'${rs.getObject("VIDEO_UUID").toString.toLowerCase}'")
  ), Some("URI"))
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
