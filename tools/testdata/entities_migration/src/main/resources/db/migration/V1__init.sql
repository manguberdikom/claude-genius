-- depot_id indeksi shu yerda, courier_id esa ataylab indekssiz.
CREATE TABLE depot (
    id bigint PRIMARY KEY,
    version bigint
);

CREATE TABLE delivery (
    id bigint PRIMARY KEY,
    version bigint,
    depot_id bigint REFERENCES depot (id),
    courier_id bigint REFERENCES depot (id),
    backup_id bigint REFERENCES depot (id),
    CONSTRAINT delivery_amount_check CHECK (id > 0),
    UNIQUE (backup_id, id)
);

CREATE INDEX IF NOT EXISTS ix_delivery_depot ON public.delivery USING btree (depot_id);
