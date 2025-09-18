#!/usr/bin/env -S scala shebang

//> using file project.scala

/*
Brian Schlining
Copyright 2022, Monterey Bay Aquarium Research Institute
*/

import java.sql.DriverManager
import java.sql.ResultSet
import java.sql.Connection
import java.util.UUID
import scala.util.Try

final case class Media(uuid: UUID, uri: String)

def lookupVideoReferencesUuids(conn: Connection): Seq[Media] = {
  val stmt = conn.createStatement()
  val rs = stmt.executeQuery("SELECT uuid, uri FROM video_references")
  val media = Seq.newBuilder[Media]
  while (rs.next()) {
    val uuid = UUID.fromString(rs.getObject("uuid").toString)
    val uri = rs.getObject("uri").toString
    media += Media(uuid, uri)
  }
  stmt.close()
  media.result()
}

def countObservationsByVideoReferenceUuuid(conn: Connection, uuid: UUID): Int = {
  val stmt = conn.createStatement()
  val rs = stmt.executeQuery(
    s"""
       |SELECT 
       |  COUNT(DISTINCT obs.uuid)
       |FROM 
       |  observations obs RIGHT JOIN
       |  imaged_moments im ON im.uuid = obs.imaged_moment_uuid
       |WHERE im.video_reference_uuid = '$uuid'
     """.stripMargin)
  rs.next()
  val n = Try(rs.getObject(1).toString.toInt).getOrElse(0)
  stmt.close()
  n
}

def compare(src: Connection, dest: Connection): Unit = {
  val sources = lookupVideoReferencesUuids(src).sortBy(_.uri)
  val targets = lookupVideoReferencesUuids(dest)
  for {
    source <- sources
  } {
    val srcN = countObservationsByVideoReferenceUuuid(src, source.uuid)
    val destN = countObservationsByVideoReferenceUuuid(dest, source.uuid)
    if (srcN == destN) {
      println(s"OK    - ${source.uri} has $srcN annotations in source and target databases")
    } else {
      println(s"ERROR - ${source.uri} is not symmetric. $srcN vs $destN annotations (source vs target)" )
    }
  }

  val leftovers = targets.diff(sources)
  for {
    missing <- leftovers
  } {
    println(s"ERROR - ${missing.uri} is missing from target database")
  }

}

def run(srcDbUrl: String,
    srcDbUser: String,
    srcDbPwd: String,
    destDbUrl: String,
    destDbUser: String,
    destDbPwd: String): Unit = {

  val src = DriverManager.getConnection(srcDbUrl, srcDbUser, srcDbPwd)
  val dest = DriverManager.getConnection(destDbUrl, destDbUser, destDbPwd)
  compare(src, dest)
  src.close()
  dest.close()
}

if (args.length != 4) {
  println("""Quick Sanity Check between two databases.
    | Usage:
    |    export SRC_PWD=<database password>
    |    export DEST_PWD=<database password>
    |    SanityCheck.sc <srcDbUrl> <srcDbUser> <destDbUrl> <destDbUser>
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
  println(s"Comparing video annotations between ${args(0)} to ${args(2)}")
  run(args(0), args(1), srcPwd, args(2), args(3), destPwd)
}