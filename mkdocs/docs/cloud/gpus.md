# GPUs

VSC Tier-1 Cloud users can also deploy VMs with different kind of GPUs.
A full GPU card is connected directly to the VM via
[PCI passthrough](https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/libvirt_application_development_guide_using_python-Guest_Domains-Device_Config-PCI_Pass.html)
and it is not shared between VMs.

See section [Instance types and flavors](flavors.md#instance-types-and-flavors)
for more information about the different GPUs available (`GPUv*` flavors).

Nvidia GPUs require the proprietary Nvidia driver to work, here it is explained how to install
and keep updated Nvidia drivers for each public OS available from VSC Tier-1 Cloud.

## Ubuntu
* Add graphics drivers ppa repo:
```shell
sudo add-apt-repository ppa:graphics-drivers/ppa
```

* Install Ubuntu drivers app:
```shell
sudo apt install ubuntu-drivers-common
```
     
* Check available GPUs:

```shell
ubuntu-drivers devices
```

```console
== /sys/devices/pci0000:00/0000:00:06.0 ==
modalias : pci:v000010DEd00001EB8sv000010DEsd000012A2bc03sc02i00
vendor   : NVIDIA Corporation
model    : TU104GL [Tesla T4]
driver   : nvidia-driver-470-server - distro non-free
driver   : nvidia-driver-515 - distro non-free
driver   : nvidia-driver-470 - distro non-free
driver   : nvidia-driver-525-server - distro non-free
driver   : nvidia-driver-418-server - distro non-free
driver   : nvidia-driver-510 - distro non-free
driver   : nvidia-driver-525 - distro non-free recommended
driver   : nvidia-driver-515-server - distro non-free
driver   : nvidia-driver-450-server - distro non-free
driver   : xserver-xorg-video-nouveau - distro free builtin
```

* Install latest Nvidia driver (change `525` with the latest version available in your case):
```shell
sudo apt install nvidia-driver-525
```

* Reboot your VM.
* Check Nvidia driver and CUDA are available after the reboot:
```console
$ nvidia-smi
Thu Feb  2 16:47:42 2023
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.78.01    Driver Version: 525.78.01    CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla T4            Off  | 00000000:00:06.0 Off |                    0 |
| N/A   45C    P8    16W /  70W |      6MiB / 15360MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                                
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A       833      G   /usr/lib/xorg/Xorg                  4MiB |
+-----------------------------------------------------------------------------+
```


## Alma Linux/CentOS/Red Hat 8.x


* Add epel repo:
```shell
sudo dnf install epel-release
```

* Add Nvidia repo:
```shell
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel8/x86_64/cuda-rhel8.repo
```

* Install Nvidia driver and cuda:
```shell
sudo dnf install nvidia-driver nvidia-driver-cuda nvidia-driver-NVML
```

* Reboot your VM.
* Check Nvidia driver and CUDA are available after the reboot:
```console
$ nvidia-smi
Thu Feb  2 15:36:40 2023       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.85.12    Driver Version: 525.85.12    CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla T4            Off  | 00000000:00:06.0 Off |                    0 |
| N/A   63C    P0    31W /  70W |      2MiB / 15360MiB |      8%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                                
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```


## Debian 11

* Install required repositories from Debian:
```shell
sudo apt install software-properties-common linux-headers-$(uname -r) -y
sudo add-apt-repository contrib
sudo add-apt-repository non-free
sudo apt install dirmngr ca-certificates software-properties-common apt-transport-https dkms curl -y
```

* Import GPG key from Nvidia repo:
```shell
curl -fSsL https://developer.download.nvidia.com/compute/cuda/repos/debian11/x86_64/3bf863cc.pub | sudo gpg --dearmor | sudo tee /usr/share/keyrings/nvidia-drivers.gpg > /dev/null 2>&1
```
 
* Import Nvidia repo:
```shell
echo 'deb [signed-by=/usr/share/keyrings/nvidia-drivers.gpg] https://developer.download.nvidia.com/compute/cuda/repos/debian11/x86_64/ /' | sudo tee /etc/apt/sources.list.d/nvidia-drivers.list
sudo apt update
sudo apt install nvidia-driver cuda nvidia-smi nvidia-settings -y
```

* Reboot your VM.
* Check Nvidia driver and CUDA are available after the reboot:
```console
$ nvidia-smi
Wed Feb  8 16:32:36 2023       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.85.12    Driver Version: 525.85.12    CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA A2           On   | 00000000:00:06.0 Off |                    0 |
|  0%   46C    P0    20W /  60W |      0MiB / 15356MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

