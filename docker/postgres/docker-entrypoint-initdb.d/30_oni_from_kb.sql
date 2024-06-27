create table Reference (LAST_UPDATED_TIME timestamp(6), id bigint not null, citation varchar(2048) not null, doi varchar(2048) unique, primary key (id));
create table Reference_ConceptDelegate (ConceptDelegateID_FK bigint not null, ReferenceID_FK bigint not null, primary key (ConceptDelegateID_FK, ReferenceID_FK));
insert into UniqueID(TableName, NextID) values ('Reference',0);
alter table if exists Reference_ConceptDelegate add constraint fk_RCD__ConceptDelegate_id foreign key (ConceptDelegateID_FK) references ConceptDelegate;
alter table if exists Reference_ConceptDelegate add constraint fk_RCD__Reference_id foreign key (ReferenceID_FK) references Reference;

ALTER TABLE Concept 
ADD COLUMN AphiaId bigint;

alter table Media
    alter column mediatype type VARCHAR(5) using mediatype::VARCHAR(5);