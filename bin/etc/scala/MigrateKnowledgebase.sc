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

def copyConcepts(src: Connection, dest: Connection): Unit = {
  println("Copying concept")
  val srcs = TableSrc("CONCEPT", 
    Seq(
      TableCol("ID", rs => rs.getLong("ID")),
      TableCol("PARENTCONCEPTID_FK", rs => rs.getLong("PARENTCONCEPTID_FK")),
      TableCol("ORIGINATOR", rs => rs.getString("ORIGINATOR")),
      TableCol("StructureType", rs => rs.getString("StructureType")),
      TableCol("REFERENCE", rs => rs.getString("REFERENCE")),
      TableCol("NODCCODE", rs => rs.getString("NODCCODE")),
      TableCol("RANKNAME", rs => rs.getString("RANKNAME")),
      TableCol("RANKLEVEL", rs => rs.getInt("RANKLEVEL")),
      TableCol("TAXONOMYTYPE", rs => rs.getString("TAXONOMYTYPE")),
      TableCol("LAST_UPDATED_TIME", rs => rs.getTimestamp("LAST_UPDATED_TIME"))
    ),
    Some("ID")
  )
  copy(srcs, src, dest)
}

def copyConceptName(src: Connection, dest: Connection): Unit = {
  println("Copying conceptname")
  val srcs = TableSrc("CONCEPTNAME", 
    Seq(
      TableCol("ID", rs => rs.getLong("ID")),
      TableCol("CONCEPTID_FK", rs => rs.getLong("CONCEPTID_FK")),
      TableCol("CONCEPTNAME", rs => rs.getString("CONCEPTNAME")),
      TableCol("AUTHOR", rs => rs.getString("AUTHOR")),
      TableCol("NAMETYPE", rs => rs.getString("NAMETYPE")),
      TableCol("LAST_UPDATED_TIME", rs => rs.getTimestamp("LAST_UPDATED_TIME"))
    )
  )
  copy(srcs, src, dest)
}

def copyConceptDelegate(src: Connection, dest: Connection): Unit = {
  println("Copying conceptdelegate")
  val srcs = TableSrc("CONCEPTDELEGATE", 
    Seq(
      TableCol("ID", rs => rs.getLong("ID")),
      TableCol("CONCEPTID_FK", rs => rs.getLong("CONCEPTID_FK")),
      TableCol("LAST_UPDATED_TIME", rs => rs.getTimestamp("LAST_UPDATED_TIME"))
    )
  )
  copy(srcs, src, dest)
}

def copyLinkTempate(src: Connection, dest: Connection): Unit = {
  println("Copying linktemplate")
  val srcs = TableSrc("LINKTEMPLATE", 
    Seq(
      TableCol("ID", rs => rs.getLong("ID")),
      TableCol("CONCEPTDELEGATEID_FK", rs => rs.getLong("CONCEPTDELEGATEID_FK")),
      TableCol("LAST_UPDATED_TIME", rs => rs.getTimestamp("LAST_UPDATED_TIME")),
      TableCol("LINKNAME", rs => rs.getString("LINKNAME")),
      TableCol("TOCONCEPT", rs => rs.getString("TOCONCEPT")),
      TableCol("LINKVALUE", rs => rs.getString("LINKVALUE"))
    )
  )
  copy(srcs, src, dest)
}

def copyHistory(src: Connection, dest: Connection): Unit = {
  println("Copying history")
  val srcs = TableSrc("HISTORY", 
    Seq(
      TableCol("ID", rs => rs.getLong("ID")),
      TableCol("CONCEPTDELEGATEID_FK", rs => rs.getLong("CONCEPTDELEGATEID_FK")),
      TableCol("LAST_UPDATED_TIME", rs => rs.getTimestamp("LAST_UPDATED_TIME")),
      TabelCol("PROCESSEDDTG", rs => rs.getTimestamp("PROCESSEDDTG")),
      TableCol("CREATEDDTG", rs => rs.getTimestamp("CREATEDDTG")),
      TableCol("DESCRIPTION", rs => rs.getString("DESCRIPTION")),
      TableCol("CREATORNAME", rs => rs.getString("CREATORNAME")),
      TableCol("PROCESSORNAME", rs => rs.getString("PROCESSORNAME")),
      TableCol("FIELD", rs => rs.getString("FIELD")),
      TableCol("OLDVALUE", rs => rs.getString("OLDVALUE")),
      TableCol("NEWVALUE", rs => rs.getString("NEWVALUE")),
      TableCol("ACTION", rs => rs.getString("ACTION")),
      TableCol("COMMENT", rs => rs.getString("COMMENT")),
      TableCol("APPROVED", rs => rs.getBoolean("APPROVED"))
    )
  )
  copy(srcs, src, dest)
}

def copyMedia(src: Connection, dest: Connection): Unit = {
  println("Copying media")
  val srcs = TableSrc("MEDIA", 
    Seq(
      TabelCol("ID", rs => rs.getLong("ID")),
      TableCol("CONCEPTDELEGATEID_FK", rs => rs.getLong("CONCEPTDELEGATEID_FK")),
      TableCol("LAST_UPDATED_TIME", rs => rs.getTimestamp("LAST_UPDATED_TIME")),
      TableCol("URL", rs => rs.getString("URL")),
      TableCol("MEDIATYPE", rs => rs.getString("MEDIATYPE")),
      TableCol("PRIMARYMEDIA", rs => rs.getBoolean("PRIMARYMEDIA")),
      TableCol("CREDIT", rs => rs.getString("CREDIT")),
      TableCol("CAPTION", rs => rs.getString("CAPTION"))
    )
  )
  copy(srcs, src, dest)
}

def copyLinkRealization(src: Connection, dest: Connection): Unit = {
  println("Copying linkrealization")
  val srcs = TableSrc("LINKREALIZATION", 
    Seq(
      TableCol("ID", rs => rs.getLong("ID")),
      TableCol("CONCEPTDELEGATEID_FK", rs => rs.getLong("CONCEPTDELEGATEID_FK")),
      TableCol("LAST_UPDATED_TIME", rs => rs.getTimestamp("LAST_UPDATED_TIME")),
      TableCol("LINKNAME", rs => rs.getString("LINKNAME")),
      TableCol("TOCONCEPT", rs => rs.getString("TOCONCEPT")),
      TableCol("LINKVALUE", rs => rs.getString("LINKVALUE"))
    )
  )
  copy(srcs, src, dest)
}

def copyPref(src: Connection, dest: Connection): Unit = {
  println("Copying prefs")
  val srcs = TableSrc("PREFS",
    Seq(
      TableCol("NODENAME", rs => rs.getString("NODENAME")),
      TableCol("PREFKEY", rs => rs.getString("PREFKEY")),
      TableCol("PREFVALUE", rs => rs.getString("PREFVALUE"))
    )
  )
  copy(srcs, src, dest)
}

def copyUserAccount(src: Connection, dest: Connection): Unit = {
  println("Copying useraccount")
  val srcs = TableSrc("USERACCOUNT", 
    Seq(
      TabelCol("ID", rs => rs.getLong("ID")),
      TableCol("USERNAME", rs => rs.getString("USERNAME")),
      TableCol("PASSWORD", rs => rs.getString("PASSWORD")),
      TableCol("ROLE", rs => rs.getString("ROLE")),
      TableCol("LAST_UPDATED_TIME", rs => rs.getTimestamp("LAST_UPDATED_TIME")),
      TableCol("AFFILIATION", rs => rs.getString("AFFILIATION")),
      TableCol("FIRSTNAME", rs => rs.getString("FIRSTNAME")),
      TableCol("LASTNAME", rs => rs.getString("LASTNAME")),
      TabelCol("EMAIL", rs => rs.getString("EMAIL"))
    )
  )
  copy(srcs, src, dest)
}

def copyUniqueID(src: Connection, dest: Connection): Unit = {
  println("Copying uniqueid")
  val srcs = TableSrc("UNIQUEID", 
    Seq(
      TableCol("NEXTID", rs => rs.getLong("NEXTID")),
      TableCol("TABLENAME", rs => rs.getString("TABLENAME"))
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
  copyConcepts(src, dest)
  copyConceptName(src, dest)
  copyConceptDelegate(src, dest)
  copyLinkRealization(src, dest)
  copyLinkTempate(src, dest)
  copyHistory(src, dest)
  copyMedia(src, dest)
  copyPref(src, dest)
  copyUserAccount(src, dest)
  copyUniqueID(src, dest)
  src.close()
  dest.close()
}

if (args.length != 4) {
  println("""Migrate Vampire-squid data to another database.
    | Usage:
    |    export SRC_PWD=<database password>
    |    export DEST_PWD=<database password>
    |    MoveVidsToAnnos.sc <srcDbUrl> <srcDbUser> <destDbUrl> <destDbUser>
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
