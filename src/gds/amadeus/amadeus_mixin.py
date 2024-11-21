class AmadeusErrorsMixin:
    QUERY_LIST_ERROR = {
        "1": "Invalid date",
        "360": "Invalid PNR file address",
        "723": "Invalid category",
        "727": "Invalid amount",
        "79A": "Invalid office identification",
        "79B": "Already working another queue",
        "79C": "Not allowed to access queues for specified office identification",
        "79D": "Queue identifier has not been assigned for specified office identification",
        "79E": "Attempting to perform a queue function when not associated with a queue",
        "79F": "Queue placement or add new queue item is not allowed for the specified office identification and queue identifier",
        "911": "Unable to process - system error",
        "912": "Incomplete message - data missing in query",
        "913": "Item/data not found or data not existing in processing host",
        "914": "Invalid format/data - data does not match EDIFACT rules",
        "915": "No action - processing host cannot support function",
        "916": "EDIFACT version not supported",
        "917": "EDIFACT message size exceeded",
        "918": "enter message in remarks",
        "919": "no PNR in AAA",
        "91A": "inactive queue bank",
        "91B": "nickname not found",
        "91C": "invalid record locator",
        "91D": "invalid format",
        "91F": "invalid queue number",
        "920": "queue/date range empty",
        "921": "target not specified",
        "922": "targetted queue has wrong queue type",
        "923": "invalid time",
        "924": "invalid date range",
        "925": "queue number not specified",
        "926": "queue category empty",
        "927": "no items exist",
        "928": "queue category not assigned",
        "929": "No more items",
        "92A": "queue category full",
    }

    PNR_RETRIEVE_LIST_ERROR = {
        "31": "Finish or ignore. There is a modified PNR present",
        "284": "Secured PNR. The user has not the rights to retrieve the PNR",
        "1929": "Invalid record locator. The record locator is not Amadeus compliant",
        "1931": "No match for rec loc. The record locator does not correspond to an active PNR",
        "3992": "Locked flight/PNR. There is an emergency lock applying to the PNR",
        "119": "Unable to retrieve PNR.	The PNR is corrupted on the database",
    }

    REMOVE_ITEM_LIST_ERROR = {
        "1": "Invalid date",
        "360": "Invalid PNR file address",
        "723": "Invalid category",
        "727": "Invalid amount",
        "79A": "Invalid office identification",
        "79B": "Already working another queue",
        "79C": "Not allowed to access queues for specified office identification",
        "79D": "Queue identifier has not been assigned for specified office identification",
        "79E": "Attempting to perform a queue function when not associated with a queue",
        "79F": "Queue placement or add new queue item is not allowed for the specified officeidentification and queue identifier",
        "911": "Unable to process - system error",
        "912": "Incomplete message - data missing in query",
        "913": "Item / data not found or data not existing in processing host",
        "914": "Invalid format / data - data does not match EDIFACT rules",
        "915": "No action - processing host cannot support function",
        "916": "EDIFACT version not supported",
        "917": "EDIFACT message size exceeded",
        "918": "enter message in remarks",
        "919": "no PNR in AAA",
        "91A": "inactive queue bank",
        "91B": "nickname not found",
        "91C": "invalid record locator",
        "91D": "invalid format",
        "91F": "invalid queue number",
        "920": "queue / date range empty",
        "921": "target not specified",
        "922": "targetted queue has wrong queue type",
        "923": "invalid time",
        "924": "invalid date range",
        "925": "queue number not specified",
        "926": "queue category empty",
        "927": "no items exist",
        "928": "queue category not assigned",
        "929": "No more items",
        "92A": "queue category full",
        "930": "Purged PNRs existed on queue.Removed from Queue",
        "931": "Purged PNRs existed on Queue.Removed from Queue",
        "932": "Restricted PNRs existed on Queue.Left on Queue",
    }


class AmadeusXMLItemsMixin:
    QUEUE_NUMBER_OF_UNITS = (
        "{http://schemas.xmlsoap.org/soap/envelope/}Body/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}Queue_ListReply/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}queueView/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}pnrCount/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}quantityDetails/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}numberOfUnit"
    )

    QUEUE_CONTROL_NUMBERS = (
        "{http://schemas.xmlsoap.org/soap/envelope/}Body/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}Queue_ListReply/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}queueView/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}item/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}recLoc/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}reservation/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}controlNumber"
    )

    QUEUE_ERROR_CODE = (
        "{http://schemas.xmlsoap.org/soap/envelope/}Body/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}Queue_ListReply/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}errorReturn/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}errorDefinition/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}errorDetails/"
        "{http://xml.amadeus.com/QDQLRR_11_1_1A}errorCode"
    )

    PNR_DELETE_ERROR_CODE = {
        "{http://schemas.xmlsoap.org/soap/envelope/}Body/"
        "{http://xml.amadeus.com/QUQMDR_03_1_1A}Queue_RemoveItemReply/"
        "{http://xml.amadeus.com/QUQMDR_03_1_1A}errorReturn/"
        "{http://xml.amadeus.com/QUQMDR_03_1_1A}errorDefinitio0n/"
        "{http://xml.amadeus.com/QUQMDR_03_1_1A}errorDetails/"
        "{http://xml.amadeus.com/QUQMDR_03_1_1A}errorCode"
    }


class AmadeusTemplatesMixin:
    QDQLRQ_11_1_1A = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1"
    xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1"
    xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1"
    xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3"
    xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
    <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
       <add:MessageID>{messageid}</add:MessageID>
       <add:Action>{action}</add:Action>
       <add:To>{To}</add:To>
       <oas:Security xmlns:oas="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:oas1="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
            <oas:UsernameToken oas1:Id="UsernameToken-1">
                 <oas:Username>{username}</oas:Username>
                 <oas:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">{nonce}</oas:Nonce>
                 <oas:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">{password}</oas:Password>
                  <oas1:Created>{created}</oas1:Created>
            </oas:UsernameToken>
       </oas:Security>
       <AMA_SecurityHostedUser xmlns="http://xml.amadeus.com/2010/06/Security_v1">
            <UserID AgentDutyCode="{agentdutycode}" RequestorType="{requestortype}" PseudoCityCode="{pseudocitycode}" POS_Type="{pos_type}"/>
       </AMA_SecurityHostedUser>
    </soapenv:Header>
    <soapenv:Body>
       <Queue_List>
                 <targetOffice>
                           <sourceType>
                                  <sourceQualifier1>{sourcequalifier1}</sourceQualifier1>
                           </sourceType>
                           <originatorDetails>
                                   <inHouseIdentification1>{inhouseidentification1}</inHouseIdentification1>
                           </originatorDetails>
                 </targetOffice>
                 <queueNumber>
                           <queueDetails>
                                     <number>{queuenumber}</number>
                           </queueDetails>
                 </queueNumber>
                 <categoryDetails>
                           <subQueueInfoDetails>
                                     <identificationType>{identificationtype}</identificationType>
                                     <itemNumber>{itemnumber}</itemNumber>
                           </subQueueInfoDetails>
                 </categoryDetails>
    </Queue_List>
    </soapenv:Body>
    </soapenv:Envelope>"""

    PNRRET_17_1_1A = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1"
                    xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1"
                    xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1"
                    xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3"
                    xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
                    <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                       <add:MessageID>{messageid}</add:MessageID>
                       <add:Action>{action}</add:Action>
                       <add:To>{to}</add:To>
                       <oas:Security xmlns:oas="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:oas1="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                            <oas:UsernameToken oas1:Id="UsernameToken-1">
                                 <oas:Username>{username}</oas:Username>
                                 <oas:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">{nonce}</oas:Nonce>
                                 <oas:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">{password}</oas:Password>
                                  <oas1:Created>{created}</oas1:Created>
                            </oas:UsernameToken>
                       </oas:Security>
                       <AMA_SecurityHostedUser xmlns="http://xml.amadeus.com/2010/06/Security_v1">
                            <UserID AgentDutyCode="{agentdutycode}" RequestorType="{requestortype}" PseudoCityCode="{}" POS_Type="{pos_type}"/>
                       </AMA_SecurityHostedUser>
                    </soapenv:Header>
                    <soapenv:Body>
                       <PNR_Retrieve xmlns="http://xml.amadeus.com/PNRRET_17_1_1A">
                           <retrievalFacts>
                               <retrieve>
                                   <type>{type}</type>
                               </retrieve>
                               <reservationOrProfileIdentifier>
                                   <reservation>
                                       <controlNumber>{controlnumber}</controlNumber>
                                   </reservation>
                               </reservationOrProfileIdentifier>
                           </retrievalFacts>
                       </PNR_Retrieve>        
                    </soapenv:Body>
                    </soapenv:Envelope>"""

    QUQMDQ_03_1_1A = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                        xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1"
                        xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1"
                        xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1"
                        xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3"
                        xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
                        <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                           <add:MessageID>{messageid}</add:MessageID>
                           <add:Action>{action}</add:Action>
                           <add:To>{to}</add:To>
                           <oas:Security xmlns:oas="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:oas1="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                                <oas:UsernameToken oas1:Id="UsernameToken-1">
                                     <oas:Username>{username}</oas:Username>
                                     <oas:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">{nonce}</oas:Nonce>
                                     <oas:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">{password}</oas:Password>
                                      <oas1:Created>{created}</oas1:Created>
                                </oas:UsernameToken>
                           </oas:Security>
                           <AMA_SecurityHostedUser xmlns="http://xml.amadeus.com/2010/06/Security_v1">
                                <UserID AgentDutyCode="{agentdutycode}" RequestorType="{requestortype}" PseudoCityCode="{}" POS_Type="{pos_type}"/>
                           </AMA_SecurityHostedUser>
                        </soapenv:Header>
                        <soapenv:Body>
                           <Queue_RemoveItem xmlns="http://xml.amadeus.com/QUQMDQ_03_1_1A">
                               <removalOption>
                                   <selectionDetails>
                                       <option>{option}</option>
                                   </selectionDetails>
                               </removalOption>
                               <targetDetails>
                                    <targetOffice>
                                        <sourceType>
                                            <sourceQualifier1>{sourcequalifier1}</sourceQualifier1>
                                        </sourceType>
                                        <originatorDetails>
                                            <inHouseIdentification1>{}</inHouseIdentification1>
                                        </originatorDetails>
                                    </targetOffice>
                                    <queueNumber>
                                        <queueDetails>
                                            <number>{queuenumber}</number>
                                        </queueDetails>
                                    </queueNumber>
                                    <categoryDetails>
                                        <subQueueInfoDetails>
                                            <identificationType>{identificationtype}</identificationType>
                                            <itemNumber>{itemnumber}</itemNumber>
                                        </subQueueInfoDetails>
                                    </categoryDetails>
                                    <recordLocator>
                                        <reservation>
                                            <controlNumber>{controlnumber}</controlNumber>
                                        </reservation>
                                    </recordLocator>
                                </targetDetails>
                           </Queue_RemoveItem>        
                        </soapenv:Body>
                        </soapenv:Envelope>"""
