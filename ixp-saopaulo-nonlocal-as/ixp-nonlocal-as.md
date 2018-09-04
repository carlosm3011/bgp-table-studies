# ASNs no-locales en IXPs LATAM

_Carlos Martinez, Marzo 2018_
_v1: 20180306_

## Objetivo y definiciones

Presentar una evolución histórica de la presencia de ASNs no locales en algunos IXPs de la región LATAM.

Definimos como AS "no local" a un AS cuyo código de país de registro no coincide con el país de registro del AS del IXP mismo.

## Fuentes de información y metodología

Utilizamos las siguientes fuentes de información:

- Información histórica de tablas de enrutamiento en IXPs
    - RIPE RIS
    - RouteViews
    - PCH LookingGlass
- Información de registro
    - RDAP / WHOIS

El análisis principal se realizó utilizando las tablas completas recolectadas por RIS, en particular por el colector localizado en el PTT de Sao Paulo (rrc15.ris.ripe.net). El criterio para determinar ASes "participantes" se basa en analizar la tabla de enrutamiento vista por rrc15 y tomar los sitemas autónomos que aparecen en primer o segundo lugar en el AS_PATH. Esto es necesario debido a que rrc15 (el colector de rutas) no tiene peering completo con todos los miembros del AS**.

## Herramientas de procesamiento

- CAIDA BGPStream

- Python 
   - ipwhois
   - ipaddr


## Lineas útiles

### Procesamiento de un archivo usango bgpstream
```
time bgpreader -w $(date +%s --date='Mar 16, 2017 0:00utc'),1489795200 -d singlefile -p ris -o rib-file,data/ris/bview.20170317.1600.gz -k 200.40.0.0/18 | ./ixpAnalysis.py

time bgpreader -w $(date +%s --date='Mar 17, 2011 0:00utc'),1489795200 -d singlefile -p ris -o rib-file,data/ris/bview.20110317.1559.gz -k 200.40.0.0/18 | ./ixpAnalysis.py

time bgpreader -w $(date +%s --date='Mar 17, 2011 0:00utc'),1489795200 -d singlefile -p ris -o rib-file,data/ris/bview.20110317.1559.gz -k 200.40.0.0/18 | ./ixpAnalysis.py
```

### Agregando código de país

```
./simplewhois.py bulk_query --outfile=data/asn.gru.cc.20110317.csv < data/asn.gru.20110317.csv 
```

### Bajando los archivos de RIS

```
cd data/ris
cat ../../source_files.csv | awk -F\| '{print $3}' | xargs -iF wget -c F
```