#!/usr/bin/env -S scala-cli shebang --scala-version 3.1.1

/*
Brian Schlining
Copyright 2022, Monterey Bay Aquarium Research Institute
*/

//> using lib "com.microsoft.sqlserver:mssql-jdbc:9.4.1.jre11"
//> using lib "com.oracle.ojdbc:ojdbc8:19.3.0.0"
//> using lib "org.apache.derby:derby:10.15.2.0"
//> using lib "org.apache.derby:derbyclient:10.15.2.0"
//> using lib "org.apache.derby:derbynet:10.15.2.0"
//> using lib "org.apache.derby:derbyshared:10.15.2.0"
//> using lib "org.jasypt:jasypt:1.9.3"
//> using lib "org.postgresql:postgresql:42.3.3"

import java.sql.Connection
import java.sql.DriverManager
import org.jasypt.util.password.BasicPasswordEncryptor

def checkUserExists(db: Connection, user: String): Boolean = {
  val stmt = db.createStatement
  val rs = stmt.executeQuery(s"select count(*) from USERACCOUNT where username = '$user'")
  rs.next
  val count = rs.getInt(1)
  rs.close
  stmt.close
  count > 0
}

def createUser(dbUrl: String, dbUser: String, dbPwd: String, username: String): Unit = {
  val connection = DriverManager.getConnection(dbUrl, dbUser, dbPwd)
  val exists = checkUserExists(connection, username)
  if (!exists) {
    println(s"Creating user '$username'")
    val console = System.console()
    val firstName = console.readLine("First name: ")
    val lastName = console.readLine("Last name: ")
    val email = console.readLine("Email: ")
    val affiliation = console.readLine("Affiliation: ")
    val pw0 = new String(console.readPassword())
    val pw1 = new String(console.readPassword())

    if (pw0 != pw1) {
      println("The passwords you entered do not match.")
    }
    else {

      require(pw0.size > 0, "Password must be at least one character long")
      require(firstName.size > 1, "First name must be at least two characters long")
      require(lastName.size > 1, "Last name must be at least two characters long")
      require(email.size > 5, "Email must be at least five characters long")      
      require(affiliation.size > 1, "Affiliation must be at least two characters long")

      val encryptor = new BasicPasswordEncryptor
      val pw = encryptor.encryptPassword(pw0)
      val stmt = connection.createStatement
      stmt.executeUpdate(s"insert into USERACCOUNT (username, firstname, lastname, email, affiliation, password) values ('$username', '$firstName', '$lastName', '$email', '$affiliation', '$pw')")
      stmt.close
      print("User created.")
    }
  }
  else {
    println(s"User '$username' already exists")
  }
  connection.close
}

if (args.length != 3) {
  println("""Create a new user in the VARS_KB database
    | 
    | Usage: 
    |   export VARS_PWD=<database password>
    |   CreateUser.sc <dbUrl> <dbUser> <username>
    |
    | Environment variables:
    |   VARS_PWD - database password
    |
    | Arguments:
    |  dbUrl: The JDBC URL of the database. e.g. For SQL Server: jdbc:sqlserver://<server>:<port>;databaseName=<database>
    |  dbUser: The database user name
    |  username: The user name to create
    |  
    |""".stripMargin('|'))
}
else {
  val dbPwd = System.getenv("VARS_PWD")
  if (dbPwd == null) {
    println("Please set an environment variable `VARS_PWD` with the VARS_KB database password")
  }
  else {
    createUser(args(0), args(1), dbPwd, args(2))
  }
  
}