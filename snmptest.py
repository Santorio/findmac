#!/usr/bin/python

import netsnmp
import sys

def GetSwitchIP(filePath):
	switchFile = open(filePath, 'r')
	snmpIPs = []
	for switchIPAddr in switchFile:
		snmpIPs.append(switchIPAddr.rstrip())
	switchFile.close()
	return snmpIPs

def GetSNMPData(IP, oid, community, VLAN):
    #Create SNMP session with device IP and return SNMP Data as list of the objects
    SNMPData = netsnmp.VarList(netsnmp.Varbind(oid))
    session = netsnmp.Session(DestHost=IP, Version=2, Community=community + VLAN)
    session.walk(SNMPData)
    return SNMPData

def macAddressToSNMPString(MAC, splitterLetter):

    mac1 = MAC.split(splitterLetter)
    listmac = []
    stringmac = ''
    for mac in mac1:
        listmac.append(str(int('0x'+ mac.lower(), 16)))
    stringmac = '.'.join(listmac)
    return stringmac

def nameOfPorts(names, ports):

        lists = {}
        for name in names:
                for port in ports:
                        if name.iid == port.val:
                                lists[port.iid] = name.val
        return lists

def switchCheck(switchIP, switchVLAN):
    SNMPInterfaceNames = GetSNMPData(switchIP, 'ifName', 'ciscoBIBclose', switchVLAN)
    SNMPInterfaceDescr = GetSNMPData(switchIP, 'ifAlias', 'ciscoBIBclose', switchVLAN)
    SNMPInterfaceIndex = GetSNMPData(switchIP, 'dot1dBasePortIfIndex', 'ciscoBIBclose', switchVLAN)
    SNMPMacAddresses = GetSNMPData(switchIP, 'dot1dTpFdbPort', 'ciscoBIBclose', switchVLAN)
    dicPorts = nameOfPorts(SNMPInterfaceNames, SNMPInterfaceIndex)
    descrPorts = nameOfPorts(SNMPInterfaceDescr, SNMPInterfaceIndex)
    macString = macAddressToSNMPString(macInput, macSplitter)
    switchCheckResult = ''
    for i in SNMPMacAddresses:
        if macString == i.iid:
            #switchCheckResult = switchCheckResult + "IP switch: " + switchIP + ' Port: ' + str(dicPorts[i.val]) + ' = ' + str(macInput) + ' ' + str(descrPorts[i.val])
			switchCheckResult = switchCheckResult + "IP switch: " + switchIP + ' Port: ' + str(dicPorts[i.val]) + ' ' + str(descrPorts[i.val])
    return switchCheckResult, dicPorts

#Input Data from command line

macInput = sys.argv[1]

macSplitter = sys.argv[2]

snmpIPs22 = GetSwitchIP('./listOfSwitches@22.txt')

snmpIPs1 = GetSwitchIP('./listOfSwitches@1.txt')


for snmpIP22 in snmpIPs22:
	Result22, dicProts22 = switchCheck(snmpIP22, '@22')
	if Result22 != '':
		print Result22
	else:
		print 'IP switch: ' + snmpIP22 + ': Nothing Found.'
for snmpIP1 in snmpIPs1:
	Result1, dicProts1 = switchCheck(snmpIP1, '@1')
	if Result1 != '':
		print Result1
	else:
		print 'IP switch: ' + snmpIP1 + ': Nothing Found.'
