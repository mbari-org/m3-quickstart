#!/usr/bin/env -S scala-cli shebang

//> using file project.scala

/*
Brian Schlining
Copyright 2022, Monterey Bay Aquarium Research Institute
*/

import java.sql.DriverManager
import org.jasypt.util.password.BasicPasswordEncryptor


def changePassword(dbUrl: String, dbUser: String, dbPwd: String, username: String): Unit = {
  println(s"Changing password for $username")
  val console = System.console()
  print("Enter the new password:")
  val pw0 = new String(console.readPassword())
  print("Enter the new password again:")
  val pw1 = new String(console.readPassword())
  if (pw0 != pw1) {
    println("The passwords you entered do not match.")
  }
  else {
    val encryptor = new BasicPasswordEncryptor()
    val encryptedPwd = encryptor.encryptPassword(pw0)
    val connection = DriverManager.getConnection(dbUrl, dbUser, dbPwd)
    val statement = connection.createStatement()
    val sql = s"""
      |UPDATE
      |  UserAccount
      |SET
      |  Password = '$encryptedPwd'
      |WHERE
      |  UserName = '${username}'
      """.stripMargin('|')
    val n = statement.executeUpdate(sql)
    if (n == 1) println("The password was succesfully changed")
    else println("Failed to change password")
  }

}

if (args.length != 3) {
  println("""Change a users password in the VARS_KB database
    | 
    | Usage: 
    |   export VARS_PWD=<database password>
    |   ChangePassword.sc <dbUrl> <dbUser> <username>
    |
    | Environment variables:
    |   VARS_PWD - database password
    |
    | Arguments:
    |  dbUrl: The JDBC URL of the database. e.g. For SQL Server: jdbc:sqlserver://<server>:<port>;databaseName=<database>
    |  dbUser: The database user name
    |  username: The user name to change the password for
    |  
    |""".stripMargin('|'))
}
else {
  val dbPwd = System.getenv("VARS_PWD")
  if (dbPwd == null) {
    println("Please set an environment variable `VARS_PWD` with the VARS_KB database password")
  }
  else {
    changePassword(args(0), args(1), dbPwd, args(2))
  }
  
}
