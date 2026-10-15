# NetTime

NetTime is a Simple Network Time Protocol (SNTP) client for Windows 95/98/Me/NT/2000/XP/Vista/7/8/10/11 and Server 2003/2008/2012/2016/2019/2022. (32 bit and 64 bit operating systems are both supported and future versions are expected to work without needing to update NetTime.)

If you're looking for a program to keep your system time accurate, you've just found it!

Its main attributes are:

- Free
- Open Source
- Small
- Easy to Install and Use
- And most importantly: **Reliable**

NetTime was originally written by Graham Mainwaring in 1997 with an open source release made in 1998. Graham made a number of updates to the program until he lost interest and finally abandoned the project officially on the 1st of July 2004.

The NetTime project has been resurrected by Mark Griffiths, who is now making an updated version available.

If you find NetTime useful, please consider making a donation to show your appreciation and to encourage further development of NetTime.

---

## Table of Contents

- [Download](#download)
- [Frequently Asked Questions (FAQs)](#frequently-asked-questions-faqs)
- [Configuration Notes](#configuration-notes)
- [Notes for Administrators](#notes-for-administrators)
- [Update History](#update-history)
- [Source Notes](#source-notes)
- [Contact](#contact)
- [Accuracy Notes](#accuracy-notes)
- [History and Other Notes](#history-and-other-notes)
- [Links](#links)

---

## Download

> **Please note:** If you get a warning from Windows Defender that the file isn't commonly downloaded, this is probably due to the files being recently signed with a new code signing certificate. If you can click **Run Anyway**, it will help with building trust in the new code signing certificate so that others don't get this false warning in future.

For technical users, you can download and compare the signed versions below with the original unsigned versions: `Unsigned/NetTimeSetup-314.exe` and `Unsigned/NetTimeSetup-320a3.exe`.

| Version | Status | Installer |
|---|---|---|
| 3.14 | Current Stable Version | `NetTimeSetup-314.exe` |
| 3.20 Alpha 1 | Previous Test Version | `NetTimeSetup-320a1.exe` |
| 3.20 Alpha 3 | Latest Test Version | `NetTimeSetup-320a3.exe` |

Previous versions as well as the source code can be downloaded from the SourceForge project page.

> **Note:** When upgrading from a previous version, you will need to shut down both the NetTime Service as well as the Tray Icon before running the installer. If you uninstall the old version first, you will need to restart your computer before starting the new installer.

---

## Frequently Asked Questions (FAQs)

### NetTime is failing to sync - it reports that all servers failed

The most common cause of this error is that a firewall is blocking the Network Time Protocol (UDP Port 123) between your system and the servers that NetTime is attempting to use. It's not always obvious that a firewall even exists, as they generally allow regular web traffic to pass normally. If you have temporarily disabled all firewalls that you know of and continue to have this problem, then it's almost certainly a firewall that you aren't aware of. If you can run a UDP traceroute to port 123 on one of the time servers that you're using, that should give you an indication of where the firewall is located.

### NetTime is failing to sync - it reports "Inconsistent responses"

If there is a large time difference between the local system and the time returned by the time server, NetTime will automatically check with a secondary server to ensure that the time it has received is actually valid. If it can't find a unique secondary server that provides a time which is a close fit to the time returned by the primary server, it will fail with "Inconsistent Responses".

The most common causes are:

- Multiple servers are configured but point to the same IP address.
- You're using the default servers and you are in a region with only 1 actual server in the NTP Pool.

Possible solutions:

- Remove all but one server address (in which case the time returned by it will always be used, even if it's invalid), or
- Change your servers. If you're using the NTP Pool servers, point to the servers for a larger geographic area.

### NetTime is syncing, but the time is out by an hour (e.g. daylight saving time isn't honoured correctly)

NetTime works internally with UTC (Universal Time) and doesn't have any code for handling daylight saving or time zones. As long as Windows is configured correctly, it should automatically handle daylight saving changes for you. If Windows isn't handling it correctly, it most likely needs to be updated. You can also manually update your time zone information using the free Microsoft tool **Windows Time Zone Editor** (`tzedit.exe`). Alternatively, the Windows Server 2003 Resource Kit Tools reportedly includes a command line `timezone.exe` tool for advanced users.

### I have configured NetTime to provide time to other systems, but it's not working

Ensure that the Windows Time Service is disabled, along with any other NTP servers that may be running. Also, make sure that the Windows Firewall and other firewalls aren't blocking the incoming connections to NetTime.

### What does Offset mean?

Offset is the time difference between the local system time and the time returned by the time server.

### What does Lag mean?

Lag is the amount of time it took for the request from NetTime to go out to the server and for the response to come back. NetTime has code to try to compensate for high latency connections, but it won't work well on connections with asymmetric network delays, i.e. when the time it takes for the request to go out is significantly different from the time for the response to come back.

### Can I configure NetTime to use a proxy server?

Unfortunately, the Network Time Protocol doesn't support the use of proxies, so that isn't an option.

### I have a problem not listed above

If NetTime isn't working correctly for you, please enable Debug level logging, attempt another time sync, and then send an email to the author with your log file attached along with a detailed description of the problem that you're having.

---

## Configuration Notes

Most settings should be fairly self explanatory, however some people have asked for clarification on certain settings:

- **Max Free Run:** Indicates how long the program will run without getting a valid sync before it considers the local time to no longer be accurate. Once this time period expires, the tray icon will change to a cross, and if it's configured to act as a time server, it will stop responding to requests for the time.
- **If Time adjustment greater than:** The default setting means that the local time will be updated regardless of how much difference there is between the current local time and the time reported by the remote server. There shouldn't normally be a reason to change this, as the current version of NetTime will check with multiple servers to ensure that it isn't using an invalid time.
- **Always provide time:** Enabling this option isn't recommended. Normally, NetTime will only provide time to other systems if it is configured to do so and it has successfully synced to an upstream server. If you enable the option to always provide time, you may find that it will give out invalid time to any systems that connect to it.

If you are using NetTime to act as a time server, you will need to disable the built-in Time Service in Windows first. Although the description for the Windows Time Service indicates that disabling it may prevent other services from loading, the author isn't currently aware of any such services that actually require it. If you're not using NetTime as a time server, disabling the Windows Time Service is optional, but there shouldn't be any harm in disabling it to save a bit of RAM.

---

## Notes for Administrators

You can quickly install the client by running the installer with either the `/silent` or `/verysilent` command line switches:

```
NetTimeSetup-314.exe /verysilent
```

If you want to preconfigure settings that are different from the defaults, they are stored in the registry under:

```
HKLM\Software\Subjective Software\NetTime
```

On 64 bit systems, the above location is remapped to:

```
HKLM\Software\Wow6432Node\Subjective Software\NetTime
```

---

## Update History

### Version 3.20 Alpha 3

- Fixed an initialization failure error.

### Version 3.20 Alpha 2

- Improved handling of Kiss of Death packets.
- Fixed handling of "unsynchronized" replies.
- Improved reporting of errors when configured to act as a time server, e.g. if Windows Time Service is still running.
- Reduced minimum retry period when not using NTP Pool Servers.
- Improved display of forms on systems with large fonts.
- If NetTime is running as a tray icon, starting the program again will show a message instructing the user to click on the tray icon.
- Fixed loading of log files containing null characters or with one or more lines without the normal CRLF pair.
- Several improvements to handling of system suspend and resume.
- Fixed handling of "Max Free Run Time".
- If time sync fails, the program won't go straight to "Time Sync Lost" status until "Max Free Run Time" has elapsed. It will now indicate "Time sync due" with an orange tray icon.
- Added description shown when viewing the list of system services.
- Reworked IPC (Inter Process Communication) code to prevent crashes from occurring under certain circumstances.
- Log Viewer will now automatically update in real time when running as a service (would previously only update if not running as a service).
- Other minor changes and fixes.

### Version 3.20 Alpha 1

- Added option to gradually correct small time errors instead of adjusting the time in one hit (thanks to code provided by Julien Blitte).
- Added log file rotation (also thanks to Julien Blitte).
- Fixed a problem with high CPU usage when a lot of logging activity was taking place.
- A few other minor improvements.

### Version 3.14

- Improved compatibility with other NTP/SNTP clients when NetTime is acting as a server, e.g. the Windows built-in time client.
- Added extra logging information.
- Fixed an error which could sometimes occur when installing over the top of a previous version.
- Fixed a problem preventing full uninstallation under certain circumstances.
- Removed requirement to manually shut down NetTime before installing a new version (a Windows restart may sometimes be required due to the above bug).
- Improved handling when service is disabled and UAC is disabled.
- Added code to re-show the tray icon after Windows Explorer crashes.
- A few other minor improvements.

### Version 3.13

- Fixed an error that caused the program to always check for updates when run as a limited user.

### Version 3.12

- Fixed an Access Violation error.

### Version 3.11

- Added a workaround for a VCL bug which could prevent the NetTime service from being installed properly in very rare circumstances.

### Version 3.1

- Fixed a problem with running on Windows NT4.
- Added a balloon tip to the tray icon when run after installation to indicate that NetTime is running.
- When set to not change time on large adjustment, will now ask the user when doing a manual check.
- Some changes to improve compatibility with newer versions of Delphi; notes added about upgrading to a newer version of the Internet Component Suite.
- Added option to always provide time when acting as a server.

### Version 3.0

- Version number change only.

### Version 3.0 Release Candidate 1

- No significant changes since Beta 4.

### Version 3.0 Beta 4

- Fixed a few more bugs introduced with Beta 2.

### Version 3.0 Beta 3

- Fixed a few bugs introduced with Beta 2.

### Version 3.0 Beta 2

- Added capability to automatically check for new versions.
- Added button to view the log within NetTime.
- Intervals can now be entered with units instead of only as a number of seconds.
- Added support for Windows Themes.
- Added option to quit if time adjustment is larger than a set value.
- Added command line option to sync only once and then exit (`/updateonce`).
- Added command line option to only attempt syncing once and exit regardless of success (`/tryonce`).

### Version 3.0 Beta 1

- Various UI fixes and improvements.
- Added default servers (thanks to the NTP Pool Project).
- Added support for the Network Time Protocol "Kiss of Death" packet.
- Added automatic syncing on additional triggers, e.g. resuming from suspend, time jumping forward or backwards.
- Added logging capability.
- Added extra information to the UI to show more details such as the time to the next sync, adjustment for the last sync, and offsets and lag for each server queried.
- Changed server query method to minimize server loads. It now queries only a single server, unless it finds a time difference of greater than 10 seconds, in which case it will check with an alternate server to ensure that an invalid time isn't used.
- Improved handling of UAC (User Account Control) under Windows Vista and 7.
- Dropped Windows 95 pseudo service. It can still be used under Windows 98/Me as a regular application.
- Removed automatic configuration screens for searching for available servers, as they are not needed with the NTP Pool default servers.
- Fixed several UI problems.
- Fixed problems with running the client under limited user accounts in conjunction with the NetTime Windows Service.
- Various other minor fixes and improvements.

Despite the amount of work that has gone into this updated version, most of the credit for it still lies with Graham Mainwaring.

---

## Source Notes

- The latest version of NetTime was compiled and tested with **Borland Delphi 7 Professional**. Earlier versions have also been tested to compile successfully with the Personal Edition of Delphi 7. If you would like to get into Delphi and make changes to NetTime, you might still be able to find a copy of Delphi 7 Personal Edition to download if you do enough searching. Alternatively, you can try the latest trial version of Delphi available from Embarcadero.
- The latest version has been tested with **Delphi XE2 Professional**. The current version includes an older version of the Internet Component Suite, which is not compatible with Unicode versions of Delphi (i.e. Delphi 2009 and newer). Upgrading to the latest version of the Internet Component Suite by François Piette will resolve the Unicode issues. When upgrading, you will need to change the reference to `HttpProt` in the `uses` clause of `UpdateCheck.pas` to read `OverbyteIcsHttpProt`.

---

## Contact

If you discover any problems with this version or would like to make a suggestion, please contact the author: **mark@timesynctool.com**

As this is free software, there are no guarantees as to when (or even if) any feature requests will be incorporated into a future version. If you have a programming project that you would like the author to work on for you, you're welcome to get in touch.

---

## Accuracy Notes

NetTime, like most SNTP clients, will generally sync your system time to within 100 milliseconds of the correct time, often within 10 milliseconds. Of course, the accuracy is highly dependent on the accuracy of the server that it is connecting to. This updated version of NetTime has improvements to try to ensure that even a badly inaccurate time server won't put the system time out (more information is included under [History and Other Notes](#history-and-other-notes)). Asymmetric latency (network delay which takes longer one way than the other) can also have an adverse impact on time accuracy.

SNTP clients resync the system time at regular intervals. Between these syncs, the system runs at its normal speed, which may mean that it runs either fast or slow, gradually putting the system time out until the next sync takes place. The speed at which the system time deviates from the correct time depends greatly on the system hardware and also, to a certain extent, on what software is being run. Most PCs gain or lose a few seconds each day. However, the author has seen a system that loses 9 seconds per hour, which is more than 3.5 minutes per day.

The vast majority of users should find that NetTime more than meets their needs. If you have specific requirements for very accurate time, it is recommended that you investigate installing a full NTP client. Although you can set NetTime to sync more frequently to compensate for an inaccurate system clock, this isn't really recommended because of the greater strain it puts on the public NTP servers. A full NTP client has extra features to ensure better time accuracy (normally well below 10 milliseconds even between time syncs) by adjusting the rate at which the system clock runs.

If you are administering a large number of PCs for an organization, it's also recommended that you configure a full NTP client on your network and have the rest of your systems sync to it with an SNTP client. This reduces the load on the public time servers even further and ensures that all systems are in sync with a single time source.

---

## History and Other Notes

Part of the apparent reason why Graham abandoned the NetTime project was that Windows 2000 and XP already include an SNTP client, and a free download was available from Microsoft for Windows NT. Graham characterized the Microsoft NTP client as being full featured. However, the current author strongly disagrees with this: the Windows SNTP client is very basic. Its user interface has only 2 features, allowing the SNTP server to be changed and a button to attempt an immediate sync. The Microsoft SNTP client does have more features available, but they require manual editing of the system registry, something which most users are understandably reluctant to do. In the end, even with editing the registry settings, the Microsoft client is still just an SNTP client with the limitation of being able to sync with only a single remote server.

Like the vast majority of SNTP clients that can only sync with one server (and also most of the remainder that only have backups for if the primary server fails completely), the Microsoft SNTP client has a major problem when it receives a reply with a vastly different time from what is currently set on the system. The software simply has no way to know which is closer to being correct: either the system time could be wildly inaccurate (e.g. because the CMOS battery has failed) or the answer from the server could be wrong (either accidentally or maliciously).

**Windows XP:** To prevent the Microsoft SNTP client from setting the system time to a wildly incorrect value, Microsoft made the design decision that their client would only update the system time if the server response was within 15 hours of the current system time. This reduced the risk of an invalid time being set on the system (but not completely), but it also has the effect that if the system time isn't at least reasonably accurate, it never will be until manually fixed. For a system with a failed CMOS battery, the Microsoft SNTP client is pretty much useless.

**Windows Vista and 7:** Microsoft relaxed the rules so that (at least when manually triggering an update) the current system time being wrong doesn't prevent the SNTP client from updating the system time. This of course means that an incorrect response from the time server can put the system time way out. The Windows Time Service in Windows 7 is also configured by default to not start automatically each time the system is started. The user interface reports that Windows is configured to automatically update the system time, but it doesn't unless the user manually starts the Windows Time Service, either through the Services Control Panel applet or by requesting a manual sync. Unless the user reconfigures the Windows Time Service to start automatically, it will be effectively disabled every time the system is restarted.

**NetTime** ensures that it is not setting the system time to an incorrect value by always checking with a second server (when configured) if the time adjustment is more than 10 seconds. Short of a major bug in the program design or a very sustained attempt to maliciously skew the system time by a rogue time server, NetTime simply won't set an invalid system time.

---

## Links

You might also be interested in:

- **FlexiRoster** - Flexible Rostering Software
- **UltraSmartCharger** - Open Source Charger/Analyzer for NiMH/NiCd/NiZn Batteries
- **GPing** - Graphical Ping
- **POP3Filter** - An Advanced Bayesian Spam Filter
- **JpegDec** - Open Source Fast JPEG Decoder for Delphi
