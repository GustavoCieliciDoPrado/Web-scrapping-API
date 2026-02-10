CREATE DATABASE property_predict_data;
\c property_predict_data
CREATE TABLE property(pp_id integer, bname varchar(30), sname varchar(40), pcode varchar(10), streetname varchar(30), PRIMARY KEY (pp_id));

CREATE TABLE tx_history(tx_id varchar(30), pp_id int, sold_date date, pp_svalue int, PRIMARY KEY(tx_id), FOREIGN KEY(pp_id) REFERENCES property(pp_id));

CREATE TABLE pp_proj_value(pp_id int, es_time_range varchar(40), es_ppvalue int, FOREIGN KEY(pp_id) REFERENCES property(pp_id));

CREATE TABLE p_atributes(pp_id int, pp_type char(20), es_type char(15), n_blt char(5), FOREIGN KEY(pp_id) REFERENCES property(pp_id));
