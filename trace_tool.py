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

import socket,subprocess,sys,os,string_handler

'''
The module responsible for probing using either traceroute or scamper.
'''
class trace_tool():

    '''
    Calls scamper and extracting the route from the text file. 
    Input: 
        a) IP_name: The IP to probe.
        b) classic: Flag to enable scamper or traceroute.
        c) arguments: The arguments of the selected tool.
    Output: 
        a) route: The IP path list.
        b) mytime: The list with the hop delays.
    '''
    def trace_call(self,IP_name,classic,arguments):
    
        # Instead of an IP address, a domain name has been given as destination to send the probe, the domain name is reversed.
        string_handle=string_handler.string_handler()
        if  not string_handle.is_valid_ip_address(IP_name,'IP'):
            try:
                IP_name=socket.gethostbyname(IP_name)
            except:
                print('Wrong address format.\nExpected an IPv4 format or a valid url.')
                exit(0)
        elif not string_handle.check_input_ip(IP_name):
            print('Wrong address format.\nExpected an IPv4 format or a valid url.')
            exit(0)

        if classic==1:      
            [route,mytime]=self.scamper_call(IP_name,arguments)
            if len(route)==0:
                print('--> Scamper returned an empty IP path. You may use "sudo" in the beginning or the scamper arguments might be wrong.')
        elif classic==0:
            [route,mytime]=self.traceroute_call(IP_name,arguments)
            if len(route)==0:
                print('--> Traceroute returned an empty IP path. You may use "sudo" in the beginning.')
                    
        return [route,mytime]


    '''
    Calls Scamper with the proper arguments and returns the hop delays in ms.
    Input:
        a) IP_name: The IP to probe.
        b) arguments: The scamper arguments. 
    Output: 
        a) route: The IP path list.
        b) mytime: The list with the hop delays.
    '''
    def scamper_call(self,IP_name,arguments):
        if arguments=='':
            whole=subprocess.getoutput('scamper -i '+IP_name)
        else:
            arguments='"trace '+arguments+' '+IP_name+'"'
            try:
                whole=subprocess.getoutput('scamper -I '+arguments)
            except:
                print('Scamper failed to traceroute. Exiting.')
                exit(0)

        splitted=whole.split('\n')
        rows=len(splitted)-1
        route=[0 for x in range(0,rows)]
        mytime=['-' for x in range(0,rows)]

        for i in range (1,rows+1):
            pos=0
            temp=splitted[i].split(' ')
            while temp[pos]=='':
                pos=pos+1
            if i>0:
                route[i-1]=temp[pos+2]
            
                if len(temp)>pos+4:
                    mytime[i-1]=temp[pos+4]+' '+temp[pos+5]
            i=i+1

        return [route,mytime]


    '''
    Calls traceroute with the proper arguments and returns the hop delays in ms.
    Input:
        a) IP_name: The IP to probe.
        b) arguments: The traceroute arguments. 
    Output: 
        a) route: The IP path list.
        b) mytime: The list with the hop delays.
    '''
    def traceroute_call(self,IP_name,arguments):
        whole=subprocess.getoutput('traceroute ' +IP_name+' '+arguments)
        splitted=whole.split('\n')
        rows=len(splitted)-1
        route=[0 for x in range(0,rows)]
        mytime=['' for x in range(0,rows)]

        for i in range (1,rows+1):
            temp=splitted[i].split('(')

            if len(temp)>1:
                temp=splitted[i].split('(')[1]
                temp=temp.split(')')[0]
                temp2=splitted[i].split(' ')
                for j in range(0,len(temp2)):
                    if temp2[j]=='ms':
                       mytime[i-1]=mytime[i-1]+' '+temp2[j-1]+' '+'ms'
            else:
                temp='*'
            route[i-1]=temp   

        return [route,mytime]