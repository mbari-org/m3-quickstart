CREATE TABLE Reference (
  LAST_UPDATED_TIME datetime2,  -- T-SQL equivalent of timestamp(6)
  id bigint NOT NULL PRIMARY KEY,
  citation nvarchar(2048) NOT NULL,
  doi nvarchar(2048) UNIQUE
);

CREATE TABLE Reference_ConceptDelegate (
  ConceptDelegateID_FK bigint NOT NULL,
  ReferenceID_FK bigint NOT NULL,
  PRIMARY KEY CLUSTERED (ConceptDelegateID_FK ASC, ReferenceID_FK ASC)  -- Clustered primary key for better performance
);


INSERT INTO UniqueID (TableName, NextID) VALUES ('Reference', 0);

ALTER TABLE Reference_ConceptDelegate
  ADD CONSTRAINT fk_RCD__ConceptDelegate_id FOREIGN KEY (ConceptDelegateID_FK)
  REFERENCES ConceptDelegate;

ALTER TABLE Reference_ConceptDelegate
  ADD CONSTRAINT fk_RCD__Reference_id FOREIGN KEY (ReferenceID_FK)
  REFERENCES Reference;

ALTER TABLE Concept
  ADD AphiaId bigint;

ALTER TABLE Media
  ALTER COLUMN mediatype nvarchar(5);