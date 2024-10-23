SET search_path = :schema;

CREATE OR REPLACE FUNCTION trip_recalculate()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    SET search_path TO :schema, public AS
    $$
        BEGIN
            IF NEW.geom IS NOT NULL THEN -- case when trip is defined manually in QGIS
                NEW.trip_distance = (SELECT ROUND((ST_Length(ST_Transform(NEW.geom, 3857)) / 1000)::NUMERIC, 2));
                NEW.pu_location_id = (SELECT l.id FROM "location" l WHERE ST_Within(ST_StartPoint(NEW.geom), l.geom));
                NEW.do_location_id = (SELECT l.id FROM "location" l WHERE ST_Within(ST_EndPoint(NEW.geom), l.geom));
            END IF;
            RETURN NEW;
        END;
    $$;

CREATE OR REPLACE TRIGGER trip_recalculate_before_insert_update
BEFORE INSERT OR UPDATE
ON trip
FOR EACH ROW
EXECUTE PROCEDURE trip_recalculate();
