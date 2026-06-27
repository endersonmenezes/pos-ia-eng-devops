build:
	podman compose build

up:
	podman compose up

down:
	podman compose down

logs:
	podman compose logs -f

restart:
	podman compose down
	podman compose up --build

clean:
	podman compose down -v