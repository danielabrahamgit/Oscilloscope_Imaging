# Oscilloscope_Imaging
Using an ESP32, the built in DACs will be fed to a two channels oscilloscope. Setting the oscilloscope to X Y will display the image. Image formatting and processing techniques will also be included. Bitluni (linked below) has been a huge source of inspiration and crafted the fast DAC libraries. This project is based off of his existing oscilloscope imaging project.

Bitluni's fast DAC library will be used in order to achieve a much faster digital to analog conversion. Here is a link to his repository:
https://github.com/bitluni/OsciDisplay/blob/master/OsciCam/FastDAC.h

Bitluni focuses on using a camera to display video to an Oscilloscope. I would reccomend watching his video in order to understand how the imaging technique will work:
https://www.youtube.com/watch?v=T_n8PtMMLiQ
