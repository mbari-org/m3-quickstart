#!/usr/bin/env -S scala-cli shebang --scala-version 3.1.1

/*

May need to drop any orphaned ConceptDelegates using:

DELETE FROM CONCEPTDELEGATE del
WHERE 
	del.ID IN (
		SELECT 
			cd.id
		FROM 	
			CONCEPTDELEGATE cd LEFT JOIN
			CONCEPT c ON c.ID = cd.CONCEPTID_FK 
		WHERE 
			c.ID IS NULL 
)

Example usage:

bin/vars_migrate_kb.sh "jdbc:derby://anicca.wifi.mbari.org:1527/VARS" varsuser "jdbc:postgresql://localhost:5432/M3_VARS?sslmode=disable&stringType=unspecified" m3

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

def copyConcepts(src: Connection, dest: Connection): Unit = {
  println("Copying concept")
  val srcs = TableSrc("concept", 
    Seq(
      ObjectCol("id", _.getLong("id")),
      ObjectCol("parentconceptid_fk", _.getLong("parentconceptid_fk")),
      StringCol("originator"),
      StringCol("structuretype"),
      StringCol("reference"),
      StringCol("nodccode"),
      StringCol("rankname"),
      StringCol("ranklevel"),
      StringCol("taxonomytype"),
      StringCol("last_updated_time")
    ),
    Some("id")
  )
  copy(srcs, src, dest)
}

def copyConceptName(src: Connection, dest: Connection): Unit = {
  println("Copying conceptname")
  val srcs = TableSrc("conceptname", 
    Seq(
      ObjectCol("id", _.getLong("id")),
      ObjectCol("conceptid_fk", _.getLong("conceptid_fk")),
      StringCol("conceptname"),
      StringCol("author"),
      StringCol("nametype"),
      StringCol("last_updated_time")
    )
  )
  copy(srcs, src, dest)
}

def copyConceptDelegate(src: Connection, dest: Connection): Unit = {
  println("Copying conceptdelegate")
  val srcs = TableSrc("conceptdelegate", 
    Seq(
      ObjectCol("id", _.getLong("id")),
      ObjectCol("conceptid_fk", _.getLong("conceptid_fk")),
      StringCol("last_updated_time")
    )
  )
  copy(srcs, src, dest)
}

def copyLinkTempate(src: Connection, dest: Connection): Unit = {
  println("Copying linktemplate")
  val srcs = TableSrc("linktemplate", 
    Seq(
      ObjectCol("id", _.getLong("id")),
      ObjectCol("conceptdelegateid_fk", _.getLong("conceptdelegateid_fk")),
      StringCol("last_updated_time"),
      StringCol("linkname"),
      StringCol("toconcept"),
      StringCol("linkvalue")
    )
  )
  copy(srcs, src, dest)
}

def copyHistory(src: Connection, dest: Connection): Unit = {
  println("Copying history")
  val srcs = TableSrc("HISTORY", 
    Seq(
      ObjectCol("id", _.getLong("id")),
      ObjectCol("conceptdelegateid_fk", _.getLong("conceptdelegateid_fk")),
      StringCol("last_updated_time"),
      StringCol("processeddtg"),
      StringCol("creationdtg"),
      StringCol("creatorname"),
      StringCol("processorname"),
      StringCol("field"),
      StringCol("oldvalue"),
      StringCol("newvalue"),
      StringCol("action"),
      StringCol("comment"),
      ObjectCol("approved", _.getBoolean("approved"))
    )
  )
  copy(srcs, src, dest)
}

def copyMedia(src: Connection, dest: Connection): Unit = {
  println("Copying media")
  val srcs = TableSrc("MEDIA", 
    Seq(
      ObjectCol("id", _.getLong("id")),
      ObjectCol("conceptdelegateid_fk", _.getLong("conceptdelegateid_fk")),
      StringCol("last_updated_time"),
      StringCol("url"),
      StringCol("mediatype"),
      ObjectCol("primarymedia", _.getBoolean("primarymedia")),
      StringCol("credit"),
      StringCol("caption")
    )
  )
  copy(srcs, src, dest)
}

def copyLinkRealization(src: Connection, dest: Connection): Unit = {
  println("Copying linkrealization")
  val srcs = TableSrc("linkrealization", 
    Seq(
      ObjectCol("id", _.getLong("id")),
      ObjectCol("conceptdelegateid_fk", _.getLong("conceptdelegateid_fk")),
      StringCol("last_updated_time"),
      StringCol("linkname"),
      StringCol("toconcept"),
      StringCol("linkvalue")
    )
  )
  copy(srcs, src, dest)
}

def copyPref(src: Connection, dest: Connection): Unit = {
  println("Copying prefs")
  val srcs = TableSrc("prefs",
    Seq(
      StringCol("nodename"),
      StringCol("prefkey"),
      StringCol("prefvalue")
    )
  )
  copy(srcs, src, dest)
}

def copyUserAccount(src: Connection, dest: Connection): Unit = {
  println("Copying useraccount")
  val srcs = TableSrc("useraccount", 
    Seq(
      ObjectCol("id", _.getLong("id")),
      StringCol("username"),
      StringCol("password"),
      StringCol("role"),
      StringCol("last_updated_time"),
      StringCol("affiliation"),
      StringCol("firstname"),
      StringCol("lastname"),
      StringCol("email")
    )
  )
  copy(srcs, src, dest)
}

def copyUniqueID(src: Connection, dest: Connection): Unit = {
  println("Copying uniqueid")
  val srcs = TableSrc("uniqueid", 
    Seq(
      ObjectCol("nextid", _.getLong("nextid")),
      StringCol("tablename")
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
