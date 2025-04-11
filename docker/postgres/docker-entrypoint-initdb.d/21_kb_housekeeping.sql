-- --------------------------------------------------------------
-- Housekeeping script to remove specific concepts and their associated names
-- First, find the concept IDs to remove
DO $$
DECLARE
  target_ids BIGINT[];
BEGIN
  SELECT array_agg(ConceptID_FK)
  INTO target_ids
  FROM ConceptName
  WHERE ConceptName IN (
    'Cydippida 2', 
    'Cydippida sp. A.', 
    'Intacta', 
    'Llyria', 
    'Marrus', 
    'Marrus claudanielis',
    'Marrus orthocanna'
    'Mertensiidae sp. A', 
    'Physonectae sp. 1', 
    'Platyctenida sp. 1', 
    'Thalassocalycida sp. 1', 
    'Thliptodon sp. A');

  -- Print the found concept IDs
  RAISE NOTICE 'Target Concept IDs: %', target_ids;

  -- Delete ConceptNames for child concepts
  DELETE FROM ConceptName
  WHERE ConceptID_FK IN (
    SELECT id FROM Concept WHERE ParentConceptID_FK = ANY(target_ids)
  );

  DELETE FROM LinkTemplate
  WHERE ConceptDelegateID_FK IN (
    SELECT cd.id
    FROM Concept AS C RIGHT JOIN
    ConceptDelegate AS cd  ON cd.ConceptID_FK = C.id
    WHERE C.id = ANY(target_ids)
  );

  DELETE FROM LinkRealization
  WHERE ConceptDelegateID_FK IN (
    SELECT cd.id
    FROM Concept AS C RIGHT JOIN
    ConceptDelegate AS cd  ON cd.ConceptID_FK = C.id
    WHERE C.id = ANY(target_ids)
  );

  DELETE FROM Media
  WHERE ConceptDelegateID_FK IN (
    SELECT cd.id
    FROM Concept AS C RIGHT JOIN
    ConceptDelegate AS cd  ON cd.ConceptID_FK = C.id
    WHERE C.id = ANY(target_ids)
  );

  DELETE FROM History
  WHERE ConceptDelegateID_FK IN (
    SELECT cd.id
    FROM Concept AS C RIGHT JOIN
    ConceptDelegate AS cd  ON cd.ConceptID_FK = C.id
    WHERE C.id = ANY(target_ids)
  );

  DELETE FROM ConceptDelegate
  WHERE id IN (
    SELECT cd.id
    FROM Concept AS C RIGHT JOIN
    ConceptDelegate AS cd  ON cd.ConceptID_FK = C.id
    WHERE C.id = ANY(target_ids)
  );

--   -- Delete child Concepts
--   DELETE FROM Concept
--   WHERE ParentConceptID_FK = ANY(target_ids);

  -- Delete ConceptNames for the target concepts
  DELETE FROM ConceptName
  WHERE ConceptID_FK = ANY(target_ids);

  -- Delete the target Concepts
  DELETE FROM Concept
  WHERE id = ANY(target_ids);

END $$;


-- --------------------------------------------------------------
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
  );

-- --------------------------------------------------------------
-- Update the URLs in the Media table
UPDATE 
  Media 
SET 
  Url = REPLACE(Url, 'http://dsg.mbari.org/images/dsg/', 'http://dsg.mbari.org/images/dsg/external/') 
WHERE 
  Url NOT LIKE 'http://dsg.mbari.org/images/dsg/external/%' AND 
  Url LIKE 'http://dsg.mbari.org/images/dsg/%';

-- Remove all internal comments ---------------------------------------
DELETE FROM 
  LinkRealization 
WHERE 
  LinkName = 'internal-video-lab-only-comment';

-- Remove bioluminescent ----------------------------------------------
DELETE FROM 
  LinkRealization 
WHERE 
  LinkName = 'is-bioluminescent';

-- Remove dsg-MBARI-new-species ---------------------------------------
DELETE FROM
  LinkRealization
WHERE
  LinkName = 'dsg-MBARI-new-species';