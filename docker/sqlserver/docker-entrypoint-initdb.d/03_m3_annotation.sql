CREATE TABLE "dbo"."ancillary_data"  ( 
	"uuid"                       	uniqueidentifier NOT NULL,
	"altitude"                   	real NULL,
	"coordinate_reference_system"	varchar(32) NULL,
	"depth_meters"               	real NULL,
	"last_updated_timestamp"     	datetime2 NULL,
	"latitude"                   	float NULL,
	"longitude"                  	float NULL,
	"oxygen_ml_per_l"            	real NULL,
	"phi"                        	float NULL,
	"xyz_position_units"         	varchar(255) NULL,
	"pressure_dbar"              	real NULL,
	"psi"                        	float NULL,
	"salinity"                   	real NULL,
	"temperature_celsius"        	real NULL,
	"theta"                      	float NULL,
	"x"                          	float NULL,
	"y"                          	float NULL,
	"z"                          	float NULL,
	"imaged_moment_uuid"         	uniqueidentifier NOT NULL,
	"light_transmission"         	real NULL,
	"rowguid"                    	uniqueidentifier ROWGUIDCOL NOT NULL CONSTRAINT "MSmerge_df_rowguid_CF72EE1FA6DD4BB8A4BBE2D3A22FDAEB" ,
	CONSTRAINT "PK__ancillar__7F4279302B7518A4" PRIMARY KEY CLUSTERED("uuid")
 ON [PRIMARY]);
CREATE TABLE "dbo"."associations"  ( 
	"uuid"                  	uniqueidentifier NOT NULL,
	"last_updated_timestamp"	datetime2 NULL,
	"link_name"             	varchar(128) NOT NULL,
	"link_value"            	varchar(1024) NULL,
	"to_concept"            	varchar(128) NULL,
	"observation_uuid"      	uniqueidentifier NOT NULL,
	"mime_type"             	varchar(64) NOT NULL,
	"rowguid"               	uniqueidentifier ROWGUIDCOL NOT NULL CONSTRAINT "MSmerge_df_rowguid_5194C31F54434E78A2686F9058CB0992" ,
	CONSTRAINT "PK__associat__7F427930B6C824FA" PRIMARY KEY CLUSTERED("uuid")
 ON [PRIMARY]);
CREATE TABLE "dbo"."image_references"  ( 
	"uuid"                  	uniqueidentifier NOT NULL,
	"description"           	varchar(256) NULL,
	"format"                	varchar(64) NULL,
	"height_pixels"         	int NULL,
	"last_updated_timestamp"	datetime2 NULL,
	"url"                   	varchar(1024) NOT NULL,
	"width_pixels"          	int NULL,
	"imaged_moment_uuid"    	uniqueidentifier NOT NULL,
	"rowguid"               	uniqueidentifier ROWGUIDCOL NOT NULL CONSTRAINT "MSmerge_df_rowguid_829FD926DB0A457FA758D7DD753E81A4" ,
	CONSTRAINT "PK__image_re__7F427930F815F257" PRIMARY KEY CLUSTERED("uuid")
 ON [PRIMARY]);
CREATE TABLE "dbo"."imaged_moments"  ( 
	"uuid"                  	uniqueidentifier NOT NULL,
	"elapsed_time_millis"   	numeric(19,0) NULL,
	"last_updated_timestamp"	datetime2 NULL,
	"recorded_timestamp"    	datetime2 NULL,
	"timecode"              	varchar(255) NULL,
	"video_reference_uuid"  	uniqueidentifier NULL,
	"rowguid"               	uniqueidentifier ROWGUIDCOL NOT NULL CONSTRAINT "MSmerge_df_rowguid_D0E359180F194E76BFF80D2159F66774" ,
	CONSTRAINT "PK__imaged_m__7F4279303DEE847D" PRIMARY KEY CLUSTERED("uuid")
 ON [PRIMARY]);
CREATE TABLE "dbo"."observations"  ( 
	"uuid"                  	uniqueidentifier NOT NULL,
	"activity"              	varchar(128) NULL,
	"concept"               	varchar(256) NULL,
	"duration_millis"       	numeric(19,0) NULL,
	"observation_group"     	varchar(128) NULL,
	"last_updated_timestamp"	datetime2 NULL,
	"observation_timestamp" 	datetime2 NULL,
	"observer"              	varchar(128) NULL,
	"imaged_moment_uuid"    	uniqueidentifier NOT NULL,
	"rowguid"               	uniqueidentifier ROWGUIDCOL NOT NULL CONSTRAINT "MSmerge_df_rowguid_87DCC5C4D532452AA8F46B0FDC85F05C" ,
	CONSTRAINT "PK__observat__7F4279305ACD8084" PRIMARY KEY CLUSTERED("uuid")
 ON [PRIMARY]);
CREATE TABLE "dbo"."video_reference_information"  ( 
	"uuid"                  	uniqueidentifier NOT NULL,
	"last_updated_timestamp"	datetime2 NULL,
	"mission_contact"       	varchar(64) NULL,
	"mission_id"            	varchar(256) NOT NULL,
	"platform_name"         	varchar(64) NOT NULL,
	"video_reference_uuid"  	uniqueidentifier NOT NULL,
	"rowguid"               	uniqueidentifier ROWGUIDCOL NOT NULL CONSTRAINT "MSmerge_df_rowguid_F1690DA155554551A98CD85D65F1471D" ,
	CONSTRAINT "PK__video_re__7F427930B246FB6C" PRIMARY KEY CLUSTERED("uuid")
 ON [PRIMARY]);
CREATE NONCLUSTERED INDEX "ids_adjust_file_histories__video_reference_uuid"
	ON "dbo"."adjust_file_histories"("video_reference_uuid");
CREATE NONCLUSTERED INDEX "idx_adjust_rov_tape_histories__video_reference_uuid"
	ON "dbo"."adjust_rov_tape_histories"("video_reference_uuid");
CREATE NONCLUSTERED INDEX "idx_ancillary_data__imaged_moment_uuid"
	ON "dbo"."ancillary_data"("imaged_moment_uuid");
CREATE NONCLUSTERED INDEX "idx_associations__link_name"
	ON "dbo"."associations"("link_name");
CREATE NONCLUSTERED INDEX "idx_associations__to_concept"
	ON "dbo"."associations"("to_concept");
CREATE NONCLUSTERED INDEX "idx_associations_link_value"
	ON "dbo"."associations"("link_value");
CREATE NONCLUSTERED INDEX "idx_image_references__imaged_moment_uuid"
	ON "dbo"."image_references"("imaged_moment_uuid");
CREATE NONCLUSTERED INDEX "idx_image_references__url"
	ON "dbo"."image_references"("url");
CREATE NONCLUSTERED INDEX "idx_imaged_moment__video_reference_uuid"
	ON "dbo"."imaged_moments"("video_reference_uuid");
CREATE NONCLUSTERED INDEX "idx_imaged_moments__elapsed_time"
	ON "dbo"."imaged_moments"("elapsed_time_millis");
CREATE NONCLUSTERED INDEX "idx_imaged_moments__recorded_timestamp"
	ON "dbo"."imaged_moments"("recorded_timestamp");
CREATE NONCLUSTERED INDEX "idx_imaged_moments__timecode"
	ON "dbo"."imaged_moments"("timecode");
CREATE NONCLUSTERED INDEX "idx_merge_rov_histories__video_reference_uuid"
	ON "dbo"."merge_rov_histories"("video_reference_uuid");
CREATE NONCLUSTERED INDEX "idx_observations__concept"
	ON "dbo"."observations"("concept");
CREATE NONCLUSTERED INDEX "idx_observations__imaged_moment_uuid"
	ON "dbo"."observations"("imaged_moment_uuid");
CREATE NONCLUSTERED INDEX "idx_video_reference_information__video_reference_uuid"
	ON "dbo"."video_reference_information"("video_reference_uuid");

ALTER TABLE "dbo"."image_references"
	ADD CONSTRAINT "UQ__image_re__DD778417265A2306"
	UNIQUE ("url") NOT ENFORCED 
	WITH (
		DATA_COMPRESSION = NONE
	) ON [PRIMARY];
ALTER TABLE "dbo"."video_reference_information"
	ADD CONSTRAINT "UQ__video_re__352A4D46EAE426D8"
	UNIQUE ("video_reference_uuid") NOT ENFORCED 
	WITH (
		DATA_COMPRESSION = NONE
	) ON [PRIMARY];
ALTER TABLE "dbo"."ancillary_data" WITH NOCHECK
	ADD CONSTRAINT "FK_ancillary_data_imaged_moment_uuid"
	FOREIGN KEY("imaged_moment_uuid")
	REFERENCES "dbo"."imaged_moments"("uuid")
	ON DELETE NO ACTION 
	ON UPDATE NO ACTION ;
ALTER TABLE "dbo"."associations"
	ADD CONSTRAINT "FK_associations_observation_uuid"
	FOREIGN KEY("observation_uuid")
	REFERENCES "dbo"."observations"("uuid")
	ON DELETE NO ACTION 
	ON UPDATE NO ACTION ;
ALTER TABLE "dbo"."image_references" WITH NOCHECK
	ADD CONSTRAINT "FK_image_references_imaged_moment_uuid"
	FOREIGN KEY("imaged_moment_uuid")
	REFERENCES "dbo"."imaged_moments"("uuid")
	ON DELETE NO ACTION 
	ON UPDATE NO ACTION ;
ALTER TABLE "dbo"."observations"
	ADD CONSTRAINT "FK_observations_imaged_moment_uuid"
	FOREIGN KEY("imaged_moment_uuid")
	REFERENCES "dbo"."imaged_moments"("uuid")
	ON DELETE NO ACTION 
	ON UPDATE NO ACTION ;
