SET search_path = :schema;

DROP TRIGGER IF EXISTS trip_recalculate_before_insert_update ON trip;
DROP FUNCTION IF EXISTS trip_recalculate();
