SET search_path = :schema;

CREATE OR REPLACE FUNCTION trip_recalculate()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    SET search_path TO :schema, public AS
    $$
        DECLARE
            v_start_location_id INT;
            v_end_location_id   INT;
            v_trip_distance     NUMERIC;
        BEGIN
            IF NEW.geom IS NOT NULL THEN -- case when trip is defined manually in QGIS
                SELECT
                    sl.id,
                    el.id,
                    ROUND((ST_Length(ST_Transform(NEW.geom, 3857)) / 1000)::NUMERIC, 2)
                INTO
                    v_start_location_id,
                    v_end_location_id,
                    v_trip_distance
                FROM trip t
                LEFT JOIN location sl ON ST_Within(ST_StartPoint(NEW.geom), sl.geom)
                LEFT JOIN location el ON ST_Within(ST_EndPoint(NEW.geom), el.geom);

                NEW.trip_distance = v_trip_distance;
                NEW.pu_location_id = v_start_location_id;
                NEW.do_location_id = v_end_location_id;
            END IF;

            RETURN NEW;
        END;
    $$;

CREATE OR REPLACE TRIGGER trip_recalculate_before_insert_update
BEFORE INSERT OR UPDATE
ON trip
FOR EACH ROW
EXECUTE PROCEDURE trip_recalculate();
