## Install EAMENA

`git clone` the project repository into `/opt/arches/eamena`
Create a virtual environment in `/opt/arches/ENV`

CD into eamena, activate the virtual environment

```bash
python -m pip install arches==7.3
python manage.py setup_db
python manage.py runserver 0:8000
```

Use PSQL to copy `auth_user` table
**Instructions for this need to be written**

Import package

```bash
python manage.py packages -o load_package -s /path/to/package/
```

## Installing in Production

In another terminal, activate the virtual environment, CD into eamena/eamena

```bash
yarn
```

Make sure `ARCHES_NAMESPACE_FOR_DATA_EXPORT` is set to the local host in `settings_local.py`

```bash
yarn build_production
```
