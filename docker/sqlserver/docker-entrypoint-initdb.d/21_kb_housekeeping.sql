-- --------------------------------------------------------------------
-- DELETE branches of concepts
-- --------------------------------------------------------------------

-- Mertensiidae sp. A  ------------------------------------------------------
DECLARE @conceptId bigint

DECLARE MyCursor CURSOR FOR
  SELECT ConceptID_FK FROM ConceptName WHERE ConceptName = 'Mertensiidae sp. A'

OPEN MyCursor
FETCH NEXT FROM MyCursor into @conceptId
WHILE @@FETCH_STATUS = 0
  BEGIN
    PRINT @conceptId
    FETCH NEXT FROM MyCursor INTO @conceptId

    -- Drop ConceptNames first
    DELETE FROM ConceptName WHERE id IN (SELECT cn.id FROM Concept AS c LEFT JOIN
      ConceptName AS cn ON cn.ConceptID_FK = c.id WHERE c.ParentConceptID_FK = @conceptId)

    -- Drop Concepts
    DELETE FROM Concept WHERE ParentConceptID_FK = @conceptId

    DELETE FROM ConceptName WHERE ConceptID_FK =@conceptId

    DELETE FROM Concept WHERE id = @conceptId

  END
CLOSE MyCursor
DEALLOCATE MyCursor

GO

-- Cydippida 2 ------------------------------------------------------
DECLARE @conceptId bigint

DECLARE MyCursor CURSOR FOR
  SELECT ConceptID_FK FROM ConceptName WHERE ConceptName = 'Cydippida 2'

OPEN MyCursor
FETCH NEXT FROM MyCursor into @conceptId
WHILE @@FETCH_STATUS = 0
  BEGIN
    PRINT @conceptId
    FETCH NEXT FROM MyCursor INTO @conceptId

    -- Drop ConceptNames first
    DELETE FROM ConceptName WHERE id IN (SELECT cn.id FROM Concept AS c LEFT JOIN
      ConceptName AS cn ON cn.ConceptID_FK = c.id WHERE c.ParentConceptID_FK = @conceptId)

    -- Drop Concepts
    DELETE FROM Concept WHERE ParentConceptID_FK = @conceptId

    DELETE FROM ConceptName WHERE ConceptID_FK =@conceptId

    DELETE FROM Concept WHERE id = @conceptId

  END
CLOSE MyCursor
DEALLOCATE MyCursor

GO

-- Cydippida sp. A. ------------------------------------------------------
DECLARE @conceptId bigint

DECLARE MyCursor CURSOR FOR
  SELECT ConceptID_FK FROM ConceptName WHERE ConceptName = 'Cydippida sp. A.'

OPEN MyCursor
FETCH NEXT FROM MyCursor into @conceptId
WHILE @@FETCH_STATUS = 0
  BEGIN
    PRINT @conceptId
    FETCH NEXT FROM MyCursor INTO @conceptId

    -- Drop ConceptNames first
    DELETE FROM ConceptName WHERE id IN (SELECT cn.id FROM Concept AS c LEFT JOIN
      ConceptName AS cn ON cn.ConceptID_FK = c.id WHERE c.ParentConceptID_FK = @conceptId)

    -- Drop Concepts
    DELETE FROM Concept WHERE ParentConceptID_FK = @conceptId

    DELETE FROM ConceptName WHERE ConceptID_FK =@conceptId

    DELETE FROM Concept WHERE id = @conceptId

  END
CLOSE MyCursor
DEALLOCATE MyCursor

GO

-- Marrus ------------------------------------------------------
DECLARE @conceptId bigint

DECLARE MyCursor CURSOR FOR
  SELECT ConceptID_FK FROM ConceptName WHERE ConceptName = 'Marrus'

OPEN MyCursor
FETCH NEXT FROM MyCursor into @conceptId
WHILE @@FETCH_STATUS = 0
  BEGIN
    PRINT @conceptId
    FETCH NEXT FROM MyCursor INTO @conceptId

    -- Drop ConceptNames first
    DELETE FROM ConceptName WHERE id IN (SELECT cn.id FROM Concept AS c LEFT JOIN
      ConceptName AS cn ON cn.ConceptID_FK = c.id WHERE c.ParentConceptID_FK = @conceptId)

    -- Drop Concepts
    DELETE FROM Concept WHERE ParentConceptID_FK = @conceptId

    DELETE FROM ConceptName WHERE ConceptID_FK =@conceptId

    DELETE FROM Concept WHERE id = @conceptId

  END
CLOSE MyCursor
DEALLOCATE MyCursor

GO


-- Llyria --------------------------------------------------
DECLARE @conceptId bigint

DECLARE MyCursor CURSOR FOR
  SELECT ConceptID_FK FROM ConceptName WHERE ConceptName = 'Llyria'

OPEN MyCursor
FETCH NEXT FROM MyCursor into @conceptId
WHILE @@FETCH_STATUS = 0
  BEGIN
    PRINT @conceptId
    FETCH NEXT FROM MyCursor INTO @conceptId

    -- Drop ConceptNames first
    DELETE FROM ConceptName WHERE id IN (SELECT cn.id FROM Concept AS c LEFT JOIN
      ConceptName AS cn ON cn.ConceptID_FK = c.id WHERE c.ParentConceptID_FK = @conceptId)

    -- Drop Concepts
    DELETE FROM Concept WHERE ParentConceptID_FK = @conceptId

    DELETE FROM ConceptName WHERE ConceptID_FK =@conceptId

    DELETE FROM Concept WHERE id = @conceptId

  END
CLOSE MyCursor
DEALLOCATE MyCursor

GO

-- Platyctenida sp. 1--------------------------------------------------
DECLARE @conceptId bigint

DECLARE MyCursor CURSOR FOR
  SELECT ConceptID_FK FROM ConceptName WHERE ConceptName = 'Platyctenida sp. 1'

OPEN MyCursor
FETCH NEXT FROM MyCursor into @conceptId
WHILE @@FETCH_STATUS = 0
  BEGIN
    PRINT @conceptId
    FETCH NEXT FROM MyCursor INTO @conceptId

    -- Drop ConceptNames first
    DELETE FROM ConceptName WHERE id IN (SELECT cn.id FROM Concept AS c LEFT JOIN
      ConceptName AS cn ON cn.ConceptID_FK = c.id WHERE c.ParentConceptID_FK = @conceptId)

    -- Drop Concepts
    DELETE FROM Concept WHERE ParentConceptID_FK = @conceptId

    DELETE FROM ConceptName WHERE ConceptID_FK =@conceptId

    DELETE FROM Concept WHERE id = @conceptId

  END
CLOSE MyCursor
DEALLOCATE MyCursor

GO

-- Thalassocalycida sp. 1 --------------------------------------------------
DECLARE @conceptId bigint

DECLARE MyCursor CURSOR FOR
  SELECT ConceptID_FK FROM ConceptName WHERE ConceptName = 'Thalassocalycida sp. 1'

OPEN MyCursor
FETCH NEXT FROM MyCursor into @conceptId
WHILE @@FETCH_STATUS = 0
  BEGIN
    PRINT @conceptId
    FETCH NEXT FROM MyCursor INTO @conceptId

    -- Drop ConceptNames first
    DELETE FROM ConceptName WHERE id IN (SELECT cn.id FROM Concept AS c LEFT JOIN
      ConceptName AS cn ON cn.ConceptID_FK = c.id WHERE c.ParentConceptID_FK = @conceptId)

    -- Drop Concepts
    DELETE FROM Concept WHERE ParentConceptID_FK = @conceptId

    DELETE FROM ConceptName WHERE ConceptID_FK =@conceptId

    DELETE FROM Concept WHERE id = @conceptId

  END
CLOSE MyCursor
DEALLOCATE MyCursor

GO

-- Intacta --------------------------------------------------
DECLARE @conceptId bigint

DECLARE MyCursor CURSOR FOR
  SELECT ConceptID_FK FROM ConceptName WHERE ConceptName = 'Intacta'

OPEN MyCursor
FETCH NEXT FROM MyCursor into @conceptId
WHILE @@FETCH_STATUS = 0
  BEGIN
    PRINT @conceptId
    FETCH NEXT FROM MyCursor INTO @conceptId

    -- Drop ConceptNames first
    DELETE FROM ConceptName WHERE id IN (SELECT cn.id FROM Concept AS c LEFT JOIN
      ConceptName AS cn ON cn.ConceptID_FK = c.id WHERE c.ParentConceptID_FK = @conceptId)

    -- Drop Concepts
    DELETE FROM Concept WHERE ParentConceptID_FK = @conceptId

    DELETE FROM ConceptName WHERE ConceptID_FK =@conceptId

    DELETE FROM Concept WHERE id = @conceptId

  END
CLOSE MyCursor
DEALLOCATE MyCursor

GO


-- Physonectae sp. 1 --------------------------------------------------
DECLARE @conceptId bigint

DECLARE MyCursor CURSOR FOR
  SELECT ConceptID_FK FROM ConceptName WHERE ConceptName = 'Physonectae sp. 1'

OPEN MyCursor
FETCH NEXT FROM MyCursor into @conceptId
WHILE @@FETCH_STATUS = 0
  BEGIN
    PRINT @conceptId
    FETCH NEXT FROM MyCursor INTO @conceptId

    -- Drop ConceptNames first
    DELETE FROM ConceptName WHERE id IN (SELECT cn.id FROM Concept AS c LEFT JOIN
      ConceptName AS cn ON cn.ConceptID_FK = c.id WHERE c.ParentConceptID_FK = @conceptId)

    -- Drop Concepts
    DELETE FROM Concept WHERE ParentConceptID_FK = @conceptId

    DELETE FROM ConceptName WHERE ConceptID_FK =@conceptId

    DELETE FROM Concept WHERE id = @conceptId

  END
CLOSE MyCursor
DEALLOCATE MyCursor

GO

-- Thliptodon sp. A --------------------------------------------------
DECLARE @conceptId bigint

DECLARE MyCursor CURSOR FOR
  SELECT ConceptID_FK FROM ConceptName WHERE ConceptName = 'Thliptodon sp. A'

OPEN MyCursor
FETCH NEXT FROM MyCursor into @conceptId
WHILE @@FETCH_STATUS = 0
  BEGIN
    PRINT @conceptId
    FETCH NEXT FROM MyCursor INTO @conceptId

    -- Drop ConceptNames first
    DELETE FROM ConceptName WHERE id IN (SELECT cn.id FROM Concept AS c LEFT JOIN
      ConceptName AS cn ON cn.ConceptID_FK = c.id WHERE c.ParentConceptID_FK = @conceptId)

    -- Drop Concepts
    DELETE FROM Concept WHERE ParentConceptID_FK = @conceptId

    DELETE FROM ConceptName WHERE ConceptID_FK =@conceptId

    DELETE FROM Concept WHERE id = @conceptId

  END
CLOSE MyCursor
DEALLOCATE MyCursor

GO

-- --------------------------------------------------------------------
-- DELETE Media and LinkRealizations from concepts
-- --------------------------------------------------------------------

DELETE FROM
  Media 
WHERE
  ConceptDelegateID_FK IN ( 
    SELECT
      cd.id
    FROM
      ConceptName AS cn RIGHT JOIN
      Concept AS C ON C.id = cn.ConceptID_FK RIGHT JOIN
      ConceptDelegate AS cd  ON cd.ConceptID_FK = C.id
    WHERE
      cn.ConceptName IN (
        'Lyroctenidae',
        'Mertensia', 
        'Platyctenida',
        'Lyroctenidae', 
        'Lyrocteis', 
        'Tjalfiellidae', 
        'Tjalfiella', 
        'Tjalfiella tristoma', 
        'Tuscaroridae',
        'Tuscarantha',
        'Tuscarantha luciae',
        'Tuscarantha braueri',
        'Tuscaretta',
        'Tuscaretta globosa',
        'Tuscaridium',
        'Tuscaridium cygneum',
        'Tuscarilla',
        'Tuscarilla nationalis',
        'Tuscarilla similis',
        'Tuscarilla campanella',
        'Tuscarora')
  )

GO

DELETE FROM
  LinkRealization 
WHERE
  ConceptDelegateID_FK IN ( 
    SELECT
      cd.id
    FROM
      ConceptName AS cn RIGHT JOIN
      Concept AS C ON C.id = cn.ConceptID_FK RIGHT JOIN
      ConceptDelegate AS cd  ON cd.ConceptID_FK = C.id
    WHERE
      cn.ConceptName IN (
        'Lyroctenidae',
        'Mertensia', 
        'Platyctenida',
        'Lyroctenidae', 
        'Lyrocteis', 
        'Tjalfiellidae', 
        'Tjalfiella', 
        'Tjalfiella tristoma', 
        'Tuscaroridae',
        'Tuscarantha',
        'Tuscarantha luciae',
        'Tuscarantha braueri',
        'Tuscaretta',
        'Tuscaretta globosa',
        'Tuscaridium',
        'Tuscaridium cygneum',
        'Tuscarilla',
        'Tuscarilla nationalis',
        'Tuscarilla similis',
        'Tuscarilla campanella',
        'Tuscarora')
  )

GO


-- Change Media references to external link ---------------------------
UPDATE 
  Media 
SET 
  Url = REPLACE(Url, 'http://dsg.mbari.org/images/dsg/', 'http://dsg.mbari.org/images/dsg/external/') 
WHERE 
  Url NOT LIKE 'http://dsg.mbari.org/images/dsg/external/%' AND 
  Url LIKE 'http://dsg.mbari.org/images/dsg/%'

GO


-- Remove all internal comments ---------------------------------------
DELETE FROM 
  LinkRealization 
WHERE 
  LinkName = 'internal-video-lab-only-comment'
GO

-- Remove bioluminescent ---------------------------------------
DELETE FROM 
  LinkRealization 
WHERE 
  LinkName = 'is-bioluminescent'
GO

-- Remove dsg-MBARI-new-species
DELETE FROM
  LinkRealization
WHERE
  LinkName = 'dsg-MBARI-new-species'
GO