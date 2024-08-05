
DNS Server Assignment Switcher 

A Python CLI tool to check and switch DNS Server in Windows. Can be used for AdBlocking and other purposes ;)


## API Reference

```cmd
switchDNS.py <Parameter>
```
Examaple: 
```cmd
python switchDNS.py flip 
```
### Parameter:

#### Check the current DNS settings

```cmd
  check
```

#### Flip the mode from current mode. (Auto to Manual / Manual to Auto)

```cmd
  flip
```
#### Switch to Automatic(DHCP)

```cmd
  auto
```
#### Switch to Manual

```cmd
  man <your_primary_dns> <your_alternate_dns>
```
Exmaple:
```cmd
  switchDNS.py man 8.8.8.8 8.0.0.8
```
