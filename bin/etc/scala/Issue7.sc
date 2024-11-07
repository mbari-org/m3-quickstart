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

val sql = """
alter table public.concept add AphiaID bigint;
alter table public.media alter column mediatype type varchar(5) using mediatype::varchar(5);
create table Reference (LAST_UPDATED_TIME timestamp(6), id bigint not null, citation varchar(2048) not null, doi varchar(2048) unique, primary key (id));
create table Reference_ConceptDelegate (ConceptDelegateID_FK bigint not null, ReferenceID_FK bigint not null, primary key (ConceptDelegateID_FK, ReferenceID_FK));
insert into UniqueID(TableName, NextID) values ('Reference',0);
create index idx_Reference_ConceptDelegate_FK1 on Reference_ConceptDelegate (ConceptDelegateID_FK);
create index idx_Reference_LUT on Reference (LAST_UPDATED_TIME);
alter table if exists Reference_ConceptDelegate add constraint fk_RCD__ConceptDelegate_id foreign key (ConceptDelegateID_FK) references ConceptDelegate;
alter table if exists Reference_ConceptDelegate add constraint fk_RCD__Reference_id foreign key (ReferenceID_FK) references Reference;
"""

def update(dbUrl: String, dbUser: String, dbPwd: String): Unit = {
  val attempt = Using(DriverManager.getConnection(dbUrl, dbUser, dbPwd)) { connection =>
    connection.setAutoCommit(false)
    val statement = connection.createStatement()
    sql.split(";").foreach { sql =>
      statement.executeUpdate(sql)
    }
    connection.commit()
  }
}

val dbPwd = System.getenv("ONI_DATABASE_PASSWORD")
val dbUrl = System.getenv("ONI_URL_FOR_APPS")
val dbUser = System.getenv("ONI_DATABASE_USER")

update(dbUrl, dbUser, dbPwd)