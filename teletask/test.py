"""Example for switching a light on and off."""
import asyncio
import random
from teletask import Teletask
from teletask.devices import Light
from teletask.devices import Dimmer

async def main():
    """Connect to KNX/IP bus, switch on light, wait 2 seconds and switch it off again."""
    doip = Teletask()
    await doip.start("192.168.1.101",55957)
    
    # light without dimmer
    light1 = Light(doip,
                  name='Stalamp1',
                  group_address_switch='32',
                  doip_component="relay")
    await light1.set_on()
    await asyncio.sleep(1)
    await light1.set_on()
    await asyncio.sleep(1)
    await light1.set_off()
    await asyncio.sleep(1)

    # light with dimmer WITH a seperate relay to turn a (dimmeable) light on/off.
    light2 = Light(doip,
                name='Stalamp2',
                group_address_switch='32',
                group_address_brightness='1',
                doip_component="relay")
    await light2.set_on()
    await asyncio.sleep(1)
    await light2.set_brightness( int(random.uniform(0, 100)) )
    await asyncio.sleep(1)
    await light2.set_off()
    await asyncio.sleep(1)
    
    # new in v1.0.4 (using new Dimmer class)
    # light with dimmer WITHOUT a seperate relay to turn a (dimmeable) light on/off.
    light3 = Dimmer(doip,
                name='Stalamp3',
                group_address_brightness='5',
                doip_component="dimmer")
    await light3.set_on()
    await asyncio.sleep(5)
    await light3.set_brightness( int(random.uniform(0, 100)) )
    await asyncio.sleep(5)
    await light3.set_off()
    await asyncio.sleep(5)

    await doip.stop()


# pylint: disable=invalid-name
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()