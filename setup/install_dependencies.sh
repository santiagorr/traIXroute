# Copyright (C) 2016 Institute of Computer Science of the Foundation for Research and Technology - Hellas (FORTH)
# Authors: Michalis Bamiedakis and George Nomikos
#
# Contact Email: gnomikos [at] ics.forth.gr
#
# This file is part of traIXroute.
#
# traIXroute is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# traIXroute is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with traIXroute.  If not, see <http://www.gnu.org/licenses/>.

OS=$(uname)

# Install dependencies for OS X.
if [ $OS == "Darwin" ]
    then
        echo "Installing dependencies in OS X."
        installer -pkg python-3.4.4-macosx10.6.pkg -target /
        xcode-select --install

# Install dependencies for Linux.
elif [ $OS == "Linux" ]
    then
        echo "Installing dependencies in Linux."
        apt-get update
        apt-get -y install g++
        apt-get -y install gcc
        apt-get -y install python3
        apt-get -y install python3-setuptools
        apt-get -y install python3-dev
        apt-get -y install traceroute
else
    echo "Error: The OS is not supported."
fi