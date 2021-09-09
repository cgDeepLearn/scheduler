--update_time_func trigger
DROP FUNCTION IF EXISTS "public"."update_time_func"();
CREATE OR REPLACE FUNCTION "public"."update_time_func"()
  RETURNS "pg_catalog"."trigger" AS $BODY$
begin
    new.update_time = current_timestamp;
    return new;
end
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

-----------
--- Table structure for t_task
------ -----
DROP TABLE IF EXISTS "t_task";
CREATE TABLE "t_task" (
  "id" SERIAL NOT NULL PRIMARY KEY,
  "name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "is_delete" bool NOT NULL DEFAULT false,
  "create_by" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "create_time" timestamp(6) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "update_by" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "update_time" timestamp(6) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
-- ----------------------------
-- Triggers structure for table t_task
-- ----------------------------
CREATE TRIGGER "t_task_update" BEFORE UPDATE ON "t_task"
FOR EACH ROW
EXECUTE PROCEDURE "update_time_func"();


-----------
--- Table structure for t_task_detail
------ -----
DROP TABLE IF EXISTS "t_task_detail";
CREATE TABLE "t_task_detail" (
  "id" SERIAL NOT NULL PRIMARY KEY,
  "task_id" INTEGER NOT NULL,
  "sub_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "trigger" json NOT NULL default '{}',
  "action" json NOT NULL default '{}',
  "is_delete" bool NOT NULL DEFAULT false,
  "create_time" timestamp(6) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
-- ----------------------------
-- Triggers structure for table t_task_detail
-- ----------------------------
CREATE TRIGGER "t_task_detail_update" BEFORE UPDATE ON "t_task_detail"
FOR EACH ROW
EXECUTE PROCEDURE "update_time_func"();
