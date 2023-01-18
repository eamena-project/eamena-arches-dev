# CHECKS

Check connections

## :electric_plug: EAMENA prod v3
> 15/11/21

- [x] AWS
  - [x] Instance state > *Running*
  - [x] Storage > Volumes > *Attached*
  - [x] Public IPv4 DNS > *Server Acceded with PuTTY/Filezilla*
  - [x] AMI > *Platform/Name/Location retrieved*
    - [x] [DB PostgreSQL](https://github.com/eamena-project/eamena-arches-dev/blob/main/check/check_db.md#floppy_disk-databases)
      - [x] PgAdmin > *PgAdmin Accessed*
        - [x] DBs names > *DBs names Accepted*
        - [x] DB pwd > *DB password Accepted*
      - [x] conf files > *`/etc/postgresql/xx/main` Accessed*
      - [x] data files > *`/var/lib/postgresql/xx/main` Accessed*
- [x] Website > https://database.eamena.org

---

## :electric_plug: EAMENA staging
> 15/11/21

- [x] AWS
  - [x] Instance state > *Running*
  - [x] Storage > Volumes > *Attached*
  - [x] Public IPv4 DNS > *Server Acceded with PuTTY/Filezilla*
  - [x] AMI > *Platform/Name/Location retrieved*
    - [x] DB PostgreSQL
      - [x] PgAdmin > *PgAdmin Accessed*
        - [x] DBs names > *DBs names Accepted*
        - [x] DB pwd > *DB password Accepted*
      - [x] conf files > *`/etc/postgresql/xx/main` Accessed*
      - [x] data files > *`/var/lib/postgresql/xx/main` Accessed*  
- [ ] Website > [eamena.training](http://eamena.training/)

---

## :electric_plug: Iraq
> 15/11/21

- [ ] AWS
  - [x] Instance state > *Running*
  - [x] Storage > Volumes > *Attached*
  - [x] Public IPv4 DNS > *Server Acceded with PuTTY/Filezilla*
  - [ ] AMI > *Platform/Name/Location retrieved*
    - [ ] DB PostgreSQL
      - [ ] PgAdmin > *PgAdmin Accessed*
        - [x] DBs names > *DBs names Accepted*
        - [x] DB pwd > *DB password Accepted*
      - [ ] conf files > *`/etc/postgresql/xx/main` Accessed*
      - [ ] data files > *`/var/lib/postgresql/xx/main` Accessed*
- [x] Website > [iraq.eamena.training](https://iraq.eamena.training/)

---

## :electric_plug: Lebanon
> 15/11/21

- [x] AWS
  - [x] Instance state > *Running*
  - [x] Storage > Volumes > *Attached*
  - [x] Public IPv4 DNS > *Server Acceded with PuTTY/Filezilla*
  - [x] AMI > *Platform/Name/Location retrieved*
    - [x] DB PostgreSQL
      - [x] PgAdmin > *PgAdmin Accessed*
        - [x] DBs names > *DBs names Accepted*
        - [x] DB pwd > *DB password Accepted*
      - [x] conf files > *`/etc/postgresql/xx/main` Accessed*
      - [x] data files > *`/var/lib/postgresql/xx/main` Accessed*
- [x] Website > [lebanon.eamena.training](https://lebanon.eamena.training/ )

---

## :electric_plug: Levant
> 15/11/21

- [x] AWS
  - [x] Instance state > *Running*
  - [x] Storage > Volumes > *Attached*
  - [x] Public IPv4 DNS > *Server Acceded with PuTTY/Filezilla*
  - [x] AMI > *Platform/Name/Location retrieved*
    - [x] DB PostgreSQL
      - [x] PgAdmin > *PgAdmin Accessed*
        - [x] DBs names > *DBs names Accepted*
        - [x] DB pwd > *DB password Accepted*
      - [x] conf files > *`/etc/postgresql/xx/main` Accessed*
      - [x] data files > *`/var/lib/postgresql/xx/main` Accessed*
- [x] Website > [levant.eamena.training](http://levant.eamena.training/)

---

## :electric_plug: YHMP
> 14/12/21

- [x] AWS
  - [x] Instance state > *Running*
  - [x] Storage > Volumes > *Attached*
  - [x] Public IPv4 DNS > *Server Acceded with PuTTY/Filezilla*
  - [x] AMI > *Platform/Name/Location retrieved*
    - [ ] DB PostgreSQL
      - [ ] PgAdmin > *PgAdmin Accessed*
        - [ ] DBs names > *DBs names Accepted*
        - [ ] DB pwd > *DB password Accepted*
      - [ ] conf files > *`/etc/postgresql/xx/main` Accessed*
      - [ ] data files > *`/var/lib/postgresql/xx/main` Accessed*
- [ ] Website > [database.yhmp.online](https://database.yhmp.online/)
