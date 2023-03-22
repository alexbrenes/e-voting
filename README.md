# Crear el bot
## Pasos
1. Enviar mensaje a `@BotFather` con el comando `/newbot`.
2. Nombrar el bot
3. Guardar el token de manera segura.

## Probar el API
```
curl -v https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe 
```

Expected output
```
< HTTP/2 200
< server: nginx/1.18.0
< date: Wed, 22 Mar 2023 01:12:29 GMT
< content-type: application/json
< content-length: 199
< strict-transport-security: max-age=31536000; includeSubDomains; preload
< access-control-allow-origin: *
< access-control-allow-methods: GET, POST, OPTIONS
< access-control-expose-headers: Content-Length,Content-Type,Date,Server,Connection
<
* Connection #0 to host api.telegram.org left intact
{"ok":true,"result":{"id":6291438683,"is_bot":true,"first_name":"PetGrupoTAA","username":"PetGrupoTAA_bot","can_join_groups":true,"can_read_all_group_messages":false,"supports_inline_queries":false}}%
```

# Ejecución
1. Instalar dependencias `pip install -r requirements.txt`
1. Copiar `botConf.json_example` a `botConf.json`
1. Sustituir el token en el archivo de configuración.
1. `python3 <nombre_bot.py>`

# Referencias
Lista de frameworks en python: https://core.telegram.org/bots/samples#python
