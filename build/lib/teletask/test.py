"""Example for switching a light on and off."""
import asyncio
import random
from teletask import Teletask
from teletask.devices import Light

async def main():
    """Connect to KNX/IP bus, switch on light, wait 2 seconds and switch it off again."""
    doip = Teletask()
    await doip.start("192.168.97.31",55957)
    light = Light(doip,
                  name='Stalamp',
                  group_address_switch='32',
                  doip_component="relay")
    await light.set_on()
    await asyncio.sleep(1)
    await light.set_on()
    await asyncio.sleep(1)
    await light.set_off()
    await asyncio.sleep(1)

    light2 = Light(doip,
                name='Stalamp',
                group_address_switch='32',
                group_address_brightness='1',
                doip_component="relay")
    await light2.set_on()
    await asyncio.sleep(1)
    await light2.set_brightness( int(random.uniform(0, 100)) )
    await asyncio.sleep(1)
    await light2.set_off()
    await asyncio.sleep(1)

    await doip.stop()


# pylint: disable=invalid-name
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()