# dk_alp
private docker-compose

require
- ubuntu :16.*, 18.*

include
- db container
    - mysql
- cache container
    - redis(include manager/slave node)
- application container
    - nginx
    - django2.2

git repository not include env and shells in local settings.
