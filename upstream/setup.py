#!/usr/bin/python3

from setuptools import setup

import subprocess, glob, os.path
import os

extra_data = []
# Build hybrid-detect on x86
if '86' in os.uname()[4]:
    subprocess.check_call(["make", "-C", "share/hybrid", "all"])
    extra_data.append(("/usr/bin/", ["share/hybrid/hybrid-detect"]))
    extra_data.append(("/etc/init/", glob.glob("share/hybrid/hybrid-gfx.conf")))

# Make the nvidia-installer hooks executable
for x in glob.glob("nvidia-installer-hooks/*"):
    os.chmod(x, 0o755)

setup(
    name="pharlap-common",
    author="Korora Project",
    author_email="dev@kororaproject.org",
    maintainer="Korora Project",
    maintainer_email="dev@kororaproject.org",
    url="http://kororaproject.org/",
    license="gpl",
    description="Detect and install additional Korora akmod driver packages",
    packages=["NvidiaDetector", "Quirks", "Pharlap"],
    data_files=[("/usr/share/pharlap-common/", ["share/obsolete", "share/fake-devices-wrapper"]),
                ("/var/lib/pharlap-common/", []),
                ("/etc/", []),
                ("/usr/share/pharlap-common/quirks", glob.glob("quirks/*")),
                ("/usr/share/pharlap-common/detect", glob.glob("detect-plugins/*")),
                ("/usr/share/doc/pharlap-common", ['README']),
                ("/usr/lib/nvidia/", glob.glob("nvidia-installer-hooks/*")),
                ("/usr/lib/ubiquity/target-config", glob.glob("ubiquity/target-config/*")),
               ] + extra_data,
    scripts=["nvidia-detector", "quirks-handler", "pharlap"],
    entry_points="""[packagekit.apt.plugins]
what_provides=Pharlap.PackageKit:what_provides
""",
)
