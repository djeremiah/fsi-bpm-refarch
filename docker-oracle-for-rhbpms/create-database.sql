
CREATE USER rhbpms IDENTIFIED BY rhbpms;
GRANT CREATE SESSION TO rhbpms;
GRANT CONNECT TO rhbpms;
GRANT RESOURCE TO rhbpms;

GRANT SELECT ON sys.dba_pending_transactions TO rhbpms;
GRANT SELECT ON sys.pending_trans$ TO rhbpms;
GRANT SELECT ON sys.dba_2pc_pending TO rhbpms;
GRANT EXECUTE ON sys.dbms_xa TO rhbpms;







