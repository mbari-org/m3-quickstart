#!/usr/bin/env -S scala shebang 


//> using dep "com.microsoft.sqlserver:mssql-jdbc:9.4.1.jre11"
//> using dep "org.postgresql:postgresql:42.7.4"

import scala.util.Failure
import scala.util.Using
import java.sql.DriverManager
import java.sql.Connection
import scala.collection.mutable.ArrayBuffer
import scala.util.Success

Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver") 
Class.forName("org.postgresql.Driver")

def fix(dbUrl: String, dbUser: String, dbPwd: String): Unit = {
    
    val attempt = Using(DriverManager.getConnection(dbUrl, dbUser, dbPwd)) { connection =>
        connection.setAutoCommit(false)
        val duplicateConceptIds = findDuplicateConceptIds(connection).toSet.toSeq.sorted
        println("Found " + duplicateConceptIds.size + " duplicate concept ids")
        for 
          id <- duplicateConceptIds
        do
          fixDuplicateConceptIds(connection, id)
        connection.commit()
    }
    attempt match {
        case Failure(e) => println(e)
        case Success(_) => ()
    }
    
}

def findDuplicateConceptIds(connection: Connection): Seq[Long] = 
    val ids = ArrayBuffer[Long]()
    Using(connection.createStatement()) { statement =>
        Using(statement.executeQuery("select conceptid_fk from conceptdelegate group by conceptid_fk having count(*) > 1")) { rs =>
            
            while (rs.next()) {
                ids += rs.getLong(1)
            }
        }
    }
    ids.toSeq

def fixDuplicateConceptIds(connection: Connection, conceptId: Long): Unit = 
    Using(connection.createStatement()) { statement =>
        Using(statement.executeQuery(s"select id from conceptdelegate where conceptid_fk = $conceptId")) { rs =>
            val ids = ArrayBuffer[Long]()
            while (rs.next()) {
                ids += rs.getLong(1)
            }
            if (ids.size > 1) {
                println("Fixing concept id: " + conceptId)
                val id = ids.head
                ids.tail.foreach { idToDelete =>
                    statement.executeUpdate(s"update linktemplate set conceptdelegateid_fk = $id where conceptdelegateid_fk = $idToDelete")
                    statement.executeUpdate(s"update linkrealization set conceptdelegateid_fk = $id where conceptdelegateid_fk = $idToDelete")
                    statement.executeUpdate(s"update media set conceptdelegateid_fk = $id where conceptdelegateid_fk = $idToDelete")
                    statement.executeUpdate(s"update history set conceptdelegateid_fk = $id where conceptdelegateid_fk = $idToDelete")
                    statement.executeUpdate(s"delete from conceptdelegate where id = $idToDelete")
                }
                connection.commit()
            }
        }
        match {
            case Failure(e) => println(e)
            case Success(_) => ()
        }
    }


val dbPwd = System.getenv("ONI_DATABASE_PASSWORD")
val dbUrl = System.getenv("ONI_URL_FOR_APPS")
val dbUser = System.getenv("ONI_DATABASE_USER")

fix(dbUrl, dbUser, dbPwd)
