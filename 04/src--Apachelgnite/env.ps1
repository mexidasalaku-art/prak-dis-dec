$env:IGNITE_VERSION = "3.1.0"

function dcu { docker compose up -d }
function dcd { docker compose down }
function dps { docker ps }

function dcli {
  docker run --rm -it --network=host -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 apacheignite/ignite:3.1.0 cli
}

function dclm {
  docker run --rm -it --network=host -v "${PWD}/sql:/opt/ignite/sql" -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 apacheignite/ignite:3.1.0 cli
}
