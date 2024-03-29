# pico-assistant
A tiny dashboard for Home Assistant, which you can build for yourself with a Raspberry Pi Pico W and a Pimoroni display module:

![Demo picture](docs/demo.jpg)

# Features

* Ability to control up to 3 devices in Home Assistant per page, using A/B/X buttons on the display as toggle controls.
* Device names + icons ([see below](#Icons)) are pulled from Home Assistant API, and highlight based on state (on/off).
* Sleep timer turns off display after 10 seconds of no input, wakes on any button press.
* A clock, which obtains time from an NTP server on boot.
* Automatic light/dark modes based on time of day.
* Support for camera entities.

# Tools

You will need:

* A [Raspberry Pi Pico W](https://www.raspberrypi.com/news/raspberry-pi-pico-w-your-6-iot-platform/).
* A [Pimoroni Pico Display Pack 2.0](https://shop.pimoroni.com/products/pico-display-pack-2-0?variant=39374122582099).
* A micro-USB cable.
* A UF2 image that supports both the Pico W & Display Pack.
  * Pimoroni's UF2 images added support for the Pico W as of version [1.19.2](https://github.com/pimoroni/pimoroni-pico/releases/tag/v1.19.2).
* A computer (presumably, the one you are reading this on!)
* [Thonny](https://thonny.org/).

Additionally, if your Pico W does not have any GPIO headers pre-attached, you will need:

* A pair of Pico GPIO header pins.
* A soldering iron + solder.
* A breadboard to align the pins while soldering.
* Some patience.

# Assembly

If your Pico W does not have GPIO headers attached already, first you will need to attach + solder them to the Pico. 

If it does, you can skip steps 1-6.

If you are not confident in soldering, ask a more experienced friend/family member/colleague for assistance - otherwise, there is plenty of material online to teach you the basics.

1) Set up your soldering station, and warm up your soldering iron. Keep it set aside for the moment.
2) Take your header pins and attach them to your breadboard. Align them with the pin spacing of the Pico, with the 'short' side of the pins facing up.
3) Slot the Pico onto the pins, making sure that the BOOTSEL button is facing up.
4) Once your soldering iron has warmed up, carefully solder each pin to each GPIO pad, making sure not to bridge any connections.
5) Once all pins are soldered, and you are confident there are no bridged connections, turn off your iron and set the breadboard + Pico aside to cool for a few minutes.
6) Gently detach the pins from the breadboard - use the plastic spacer for purchase if needed.
7) Attach the Pico Display Pack 2.0 to the GPIO pins - this should be fairly self explanatory - the display pack has a diagram on its reverse showing the correct orientation of the Pico.

# Configuration

First, clone the contents of this repo to your local machine.

## Pico Setup

While holding down the BOOTSEL button on your Pico, connect it to your device via micro-USB cable.

The Pico should present itself as a USB mass storage drive.

Copy the `.UF2` file that you obtained for this project to the root of the drive. Once copied, the storage drive will automatically disconnect, and the Pico is ready for use.

## Basic Config

Next, open the following files in the text editor of your choice: `config.py` and `secrets.py`.

In `secrets.py`, you need to provide:

* The SSID and password for your WiFi network.
* The long-lived access token for your Home Assistant instance. 
  * Instructions on generating such tokens can be found [here](https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token).

In `config.py`, you need to provide:

* Your timezone, in UTC offset:
  * For example: EST would be -5, GMT would be 0, NPT would be 5.75, etc.
* Whether your timezone uses DST, and if so:
  * The start date of DST in your timezone.
  * The end date of DST in your timezone.
  * The number of hours shifted during DST (in most of the world this would be 1, in rare cases it may be a fraction e.g. 0.5).
* The base URL of your Home Assistant instance.
* Area configuration; see below.

## Area Config

`config.py` contains a dictionary that defines the "areas" you wish to control. This does not map to the concept of Areas in Home Assistant, as that functionality is not exposed via the HA API; instead, think of these as pages on the display which you can cycle through.

An area can be configured in one of three ways:

1) Device Control: An area can support displaying or controlling up to three devices in Home Assistant (the Display Pack has 4 buttons, so 3 can be used as a toggle control for each device, the fourth button is used to switch areas). The value for each Area key is a nested array of dictionaries that define the entity ID and (optionally) a toggle service for each device in the area. If no toggle service is defined, the associated button does nothing.
2) Camera: An area can contain a single entity in the `camera` domain. In this mode, no other devices can be controlled, and the entire page shows just the latest snapshot image from the camera entity (live video is not supported). It is recommended to reference a [camera_proxy](https://www.home-assistant.io/integrations/proxy/) entity instead of an actual camera, and set the `max_image_width` and `max_image_height` of the proxy entity to 320x240.
3) Climate: In this mode, an area is set up to view and control a single entity in the `climate` domain. The current and target temperatures associated with the entity are displayed on the screen, and the A and B buttons are used to increment or decrement the target temperature in offsets of one degree.

An example configuration has been provided in `config.py` for reference.

If you add more than 3 devices (or more than a single camera or climate entity) to an area configuration, the additional devices will be ignored.

## First Run

Once the above steps are complete, connect your Pico W to your machine and open Thonny. Make sure to select the Pico's MicroPython environment on the bottom-right of the Thonny window, then, once connected, upload each of the `.py` files to your device.

**NOTE:** Depending on the UF2 image that you used, you *might* need to install the `urequests` package before running the display for the first time. To do this, uncomment the relavent lines in `api.py`, save to the Pico and then run `main.py` once manually in order for the Pico to connect to your network and install the package. Alternatively, you can install `urequests` to the Pico via Thonny's package manager.

Once installed, stop execution, re-comment or delete the lines, save and re-upload to the Pico.

The application will now auto-start whenever you supply power to your Pico.

## Icons

Due to the extreme resource constraints on a Pico, especially given the fact we are driving a display AND a WLAN device in the background, the way in which we draw icons for each device is fairly primitive.

Home Assistant uses [Material Design Icons](https://materialdesignicons.com/), and it is trivial to obtain the icon name for a given device from its API, which in turn we can use to obtain an SVG file from MDI. 

However, having the Pico both render AND draw a SVG image currently appears to be beyond its capabilities. No micropython SVG libraries currently seem to exist, perhaps for good reason; I did attempt to hand-roll an *extremely* basic SVG command parser + polygon transform function, but this resulted in the Pico hard locking and requiring a power cycle on every render attempt.

Hence, instead of having the Pico render the SVG itself, we can do half of the work for it by manually transforming each required icon into a list of tuples representing a polygon, which the Display Pack's graphics library is able to draw.

So, for each MDI icon name that is referenced in your HA instance, and that you want represented on this dashboard, you will need to obtain an SVG image to represent it (this of course could be any SVG that you like), and then run a transform operation to obtain point co-ordinates from the SVG path commands.

There is a helpful tool by [@betravis](https://betravis.github.io/) available [here](https://betravis.github.io/shape-tools/path-to-polygon/) that will do this for you for any given SVG file. However, note that the polygon co-ordinates need to be integers, not floats, so some manual rounding will be required, which could result in certain icons not appearing quite as expected.

Once you have the tuple array, you will need to add it to the dictionary in `icons.py`, using the MDI icon name as the key. Some examples have been provided in that file for reference, as well as a default icon that is used as a fallback if the icon name cannot be found in the dictionary.

### Caveats:
 * If your icon polygon is beyond a certain size / complexity, it may still crash your Pico. Hence, you might have to find some lower complexity alternatives for certain MDI icons.
 * If your device shows with the default icon even if it has been added to the dictionary in `icons.py`, check the device in your Home Assistant Lovelace frontend; if the icon is inherited based on device class, you may find that you have to explicitly assign an icon to the device via Lovelace in order for the Home Assistant API to present that information.
