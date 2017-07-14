
#include "ws.h"


//==============================================================================
/* Declaration */

/*!
 * @addtogroup WS_API 
 * 
 * @{
 */

/*!
 * @name private interface of ws dll
 * @{
 */

static HRESULT WS_CALL ws_enable_sharing_eth(INetSharingManager* pNSM, const wchar_t* eth_name);
static HRESULT WS_CALL ws_enable_sharing_hn(INetSharingManager* pNSM);
static HRESULT WS_CALL ws_disable_sharing_eht_hn(INetSharingManager* pNSM, const wchar_t* eth_name);

/*! @} */
/*! @} */

/* Declaration End */
//==============================================================================


//==============================================================================
/*!
 * @brief enable sharing connections.
 *
 * @param eth_name: the name of network connection to be shared public
 * @return 
 * @retval 
 */
//==============================================================================
WS_API int WS_CALL ws_enable_sharing(const wchar_t* eth_name)
{
    // 初始化COM库以供调用线程使用
    CoInitialize(NULL);

    // init security to enum RAS connections
    CoInitializeSecurity(NULL, -1, NULL, NULL,
                        RPC_C_AUTHN_LEVEL_PKT,
                        RPC_C_IMP_LEVEL_IMPERSONATE,
                        NULL, EOAC_NONE, NULL);

    // INetSharingManager: Primary interface for Manager object
    INetSharingManager* pNSM = NULL;

    // 用指定的类标识符创建一个Com对象
    HRESULT hr = ::CoCreateInstance(__uuidof(NetSharingManager),
                        NULL,
                        CLSCTX_ALL,
                        __uuidof(INetSharingManager),
                        (void**)&pNSM);
    if (!pNSM)
    {
        CoUninitialize();
        return WS_ERR_CREATE;
    }
    else
    {
        // must enable sharing of ethernet connetion first
        hr = ws_enable_sharing_eth(pNSM, eth_name);
        if(hr != S_OK)
        {
            CoUninitialize();
            return WS_ERR_SHARE_EN_ETH;
        }

        hr = ws_enable_sharing_hn(pNSM);
        if(hr != S_OK)
        {
            CoUninitialize();
            return WS_ERR_SHARE_EN_HN;
        }
    }

    CoUninitialize();

    return WS_OK;
}


//==============================================================================
/*!
 * @brief disable sharing connections.
 *
 * @param eth_name: the name of network connection to be shared public
 * @return 
 * @retval 
 */
//==============================================================================
WS_API int WS_CALL ws_disable_sharing(const wchar_t* eth_name)
{
    // 初始化COM库以供调用线程使用
    CoInitialize(NULL);

    // init security to enum RAS connections
    CoInitializeSecurity(NULL, -1, NULL, NULL,
                        RPC_C_AUTHN_LEVEL_PKT,
                        RPC_C_IMP_LEVEL_IMPERSONATE,
                        NULL, EOAC_NONE, NULL);

    // INetSharingManager: Primary interface for Manager object
    INetSharingManager * pNSM = NULL;

    // 用指定的类标识符创建一个Com对象
    HRESULT hr = ::CoCreateInstance(__uuidof(NetSharingManager),
                        NULL,
                        CLSCTX_ALL,
                        __uuidof(INetSharingManager),
                        (void**)&pNSM);
    if (!pNSM)
    {
        CoUninitialize();
        return WS_ERR_CREATE;
    }
    else
    {
        hr = ws_disable_sharing_eht_hn(pNSM, eth_name);
    }

    CoUninitialize();

    if(hr != S_OK)
        return WS_ERR_SHARE_DIS;
    else
        return WS_OK;
}


//==============================================================================
/*!
 * @brief enable ethernet-connection sharing.
 *
 * @param pNSM: INetSharingManager object
 * @param eth_name: the name of network connection to be shared public
 * @return
 * @retval
 */
//==============================================================================
static HRESULT WS_CALL ws_enable_sharing_eth(INetSharingManager* pNSM, const wchar_t* eth_name)
{
    // INetConnection: Primary interface for managing network conections
    INetConnection * pNC = NULL;

    // Collection interface for all connections
    INetSharingEveryConnectionCollection * pNSECC = NULL;

    // get and enumerate all connections
    HRESULT hr = pNSM->get_EnumEveryConnection (&pNSECC);
    if (!pNSECC)
        return hr;
    else 
    {
        // enumerate connections
        IEnumVARIANT * pEV = NULL;
        IUnknown * pUnk = NULL;
        hr = pNSECC->get__NewEnum (&pUnk);
        if (pUnk) 
        {
            hr = pUnk->QueryInterface (__uuidof(IEnumVARIANT), (void**)&pEV);
            pUnk->Release();
        }

        if (pEV) 
        {
            VARIANT v;
            VariantInit (&v);
            while (S_OK == pEV->Next (1, &v, NULL)) 
            {
                if (V_VT (&v) == VT_UNKNOWN) 
                {
                    V_UNKNOWN (&v)->QueryInterface (__uuidof(INetConnection), (void**)&pNC);
                    if (pNC) 
                    {
                        // get connection properties
                        NETCON_PROPERTIES* pNP = NULL;
                        pNC->GetProperties(&pNP);

                        // ethernet
                        if (!std::strcmp((char*)pNP->pszwName, (char*)eth_name))
                        {
                            // INetSharingConfiguration: manage connection sharing, port mapping, and Internet
                            INetSharingConfiguration * pNSC = NULL;
                            hr = pNSM->get_INetSharingConfigurationForINetConnection (pNC, &pNSC);
                            if (!pNSC) 
                            {
                                return hr;
                            }
                            else
                            {
                                pNSC->EnableSharing(ICSSHARINGTYPE_PUBLIC);
                                pNSC->Release();
                            }
                        }
                        pNC->Release();
                    }
                }
                VariantClear (&v);
            }
            pEV->Release();
        }
        pNSECC->Release();
    }
    return hr;
}


//==============================================================================
/*!
 * @brief enable sharing hostednetwork-connection.
 *
 * @param pNSM: INetSharingManager object
 * @return
 * @retval
 */
//==============================================================================
static HRESULT WS_CALL ws_enable_sharing_hn(INetSharingManager *pNSM)
{
    // INetConnection: Primary interface for managing network conections
    INetConnection * pNC = NULL;

    // Collection interface for all connections
    INetSharingEveryConnectionCollection * pNSECC = NULL;

    // get and enumerate all connections
    HRESULT hr = pNSM->get_EnumEveryConnection (&pNSECC);
    if (!pNSECC)
        return hr;
    else 
    {
        // enumerate connections
        IEnumVARIANT * pEV = NULL;
        IUnknown * pUnk = NULL;
        hr = pNSECC->get__NewEnum (&pUnk);
        if (pUnk) 
        {
            hr = pUnk->QueryInterface (__uuidof(IEnumVARIANT), (void**)&pEV);
            pUnk->Release();
        }

        if (pEV) 
        {
            VARIANT v;
            VariantInit (&v);
            while (S_OK == pEV->Next (1, &v, NULL)) 
            {
                if (V_VT (&v) == VT_UNKNOWN) 
                {
                    V_UNKNOWN (&v)->QueryInterface (__uuidof(INetConnection), (void**)&pNC);
                    if (pNC) 
                    {
                        // get connection properties
                        NETCON_PROPERTIES* pNP = NULL;
                        pNC->GetProperties(&pNP);

                        // hosted-network
                        if(pNP->dwCharacter & NCCF_HOSTED_NETWORK)
                        { 
                            // INetSharingConfiguration: manage connection sharing, port mapping, and Internet
                            INetSharingConfiguration * pNSC = NULL;
                            hr = pNSM->get_INetSharingConfigurationForINetConnection (pNC, &pNSC);
                            if (!pNSC) 
                            {
                                return hr;
                            }
                            else
                            {
                                pNSC->EnableSharing(ICSSHARINGTYPE_PRIVATE);
                                pNSC->Release();
                            }
                        }
                        pNC->Release();
                    }
                }
                VariantClear (&v);
            }
            pEV->Release();
        }
        pNSECC->Release();
    }
    return hr;
}


//==============================================================================
/*!
 * @brief disable sharing of ethernet and hostednetwork connections.
 *
 * @param pNSM: INetSharingManager object
 * @param eth_name: the name of network connection to be shared public
 * @return
 * @retval
 */
//==============================================================================
static HRESULT WS_CALL ws_disable_sharing_eht_hn(INetSharingManager* pNSM, const wchar_t* eth_name)
{
    // INetConnection: Primary interface for managing network conections
    INetConnection * pNC = NULL;

    // Collection interface for all connections
    INetSharingEveryConnectionCollection * pNSECC = NULL;

    // get and enumerate all connections
    HRESULT hr = pNSM->get_EnumEveryConnection (&pNSECC);
    if (!pNSECC)
        return hr;
    else 
    {
        // enumerate connections
        IEnumVARIANT * pEV = NULL;
        IUnknown * pUnk = NULL;
        hr = pNSECC->get__NewEnum (&pUnk);
        if (pUnk) 
        {
            hr = pUnk->QueryInterface (__uuidof(IEnumVARIANT), (void**)&pEV);
            pUnk->Release();
        }

        if (pEV) 
        {
            VARIANT v;
            VariantInit (&v);
            while (S_OK == pEV->Next (1, &v, NULL)) 
            {
                if (V_VT (&v) == VT_UNKNOWN) 
                {
                    V_UNKNOWN (&v)->QueryInterface (__uuidof(INetConnection), (void**)&pNC);
                    if (pNC) 
                    {
                        // get connection properties
                        NETCON_PROPERTIES* pNP = NULL;
                        pNC->GetProperties(&pNP);

                        // hosted-network
                        if(pNP->dwCharacter & NCCF_HOSTED_NETWORK)
                        { 
                            // INetSharingConfiguration: manage connection sharing, port mapping, and Internet
                            INetSharingConfiguration * pNSC = NULL;
                            hr = pNSM->get_INetSharingConfigurationForINetConnection (pNC, &pNSC);
                            if (!pNSC) 
                            {
                                return hr;
                            }
                            else
                            {
                                pNSC->DisableSharing();
                                pNSC->Release();
                            }
                        }

                        // ethernet
                        if (!std::strcmp((char*)pNP->pszwName, (char*)eth_name))
                        {
                            // INetSharingConfiguration: manage connection sharing, port mapping, and Internet
                            INetSharingConfiguration * pNSC = NULL;
                            hr = pNSM->get_INetSharingConfigurationForINetConnection (pNC, &pNSC);
                            if (!pNSC) 
                            {
                                return hr;
                            }
                            else
                            {
                                pNSC->DisableSharing();
                                pNSC->Release();
                            }
                        }
                        pNC->Release();
                    }
                }
                VariantClear (&v);
            }
            pEV->Release();
        }
        pNSECC->Release();
    }
    return hr;
}


//==============================================================================
/*!
 * @brief get all connections.
 *
 * @param num: store the number of connection
 * @param name: the vector store all connections
 * @return
 * @retval
 */
//==============================================================================
WS_API int WS_CALL ws_get_connections(long* num, std::vector<std::wstring>* name)
{
    // 初始化COM库以供调用线程使用
    CoInitialize(NULL);

    // init security to enum RAS connections
    CoInitializeSecurity(NULL, -1, NULL, NULL,
                        RPC_C_AUTHN_LEVEL_PKT,
                        RPC_C_IMP_LEVEL_IMPERSONATE,
                        NULL, EOAC_NONE, NULL);

    // INetSharingManager: Primary interface for Manager object
    INetSharingManager* pNSM = NULL;

    // 用指定的类标识符创建一个Com对象
    HRESULT hr = ::CoCreateInstance(__uuidof(NetSharingManager),
                        NULL,
                        CLSCTX_ALL,
                        __uuidof(INetSharingManager),
                        (void**)&pNSM);
    if (!pNSM)
    {
        CoUninitialize();
        return WS_ERR_CREATE;
    }
    else
    {
        // INetConnection: Primary interface for managing network conections
        INetConnection * pNC = NULL;

        // Collection interface for all connections
        INetSharingEveryConnectionCollection * pNSECC = NULL;

        // get and enumerate all connections
        HRESULT hr = pNSM->get_EnumEveryConnection (&pNSECC);
        if (!pNSECC)
            return WS_ERR_GET_CONNECTION;
        else 
        {
			// get connection count
			pNSECC->get_Count(num);

            // enumerate connections
            IEnumVARIANT * pEV = NULL;
            IUnknown * pUnk = NULL;
            hr = pNSECC->get__NewEnum (&pUnk);
            if (pUnk) 
            {
                hr = pUnk->QueryInterface (__uuidof(IEnumVARIANT), (void**)&pEV);
                pUnk->Release();
            }

            if (pEV) 
            {
                VARIANT v;
                VariantInit (&v);
                while (S_OK == pEV->Next (1, &v, NULL)) 
                {
                    if (V_VT (&v) == VT_UNKNOWN) 
                    {
                        V_UNKNOWN (&v)->QueryInterface (__uuidof(INetConnection), (void**)&pNC);
                        if (pNC) 
                        {
                            // get connection properties
                            NETCON_PROPERTIES* pNP = NULL;
                            pNC->GetProperties(&pNP);
							name->push_back(pNP->pszwName);
                            pNC->Release();
                        }
                    }
                    VariantClear (&v);
                }
                pEV->Release();
            }
            pNSECC->Release();
        }
        return hr;
    }

    CoUninitialize();
    return WS_OK;
}

//==============================================================================
/*!
 * @brief convert vector to python-tuple.
 * This function is used for python script
 *
 * @param ret: the return result of ws_get_connection
 * @return return py-list to python to use
 * @retval
 */
//==============================================================================
WS_API PyObject* WS_CALL ws_py_get_connections(int* ret)
{
    std::vector<std::wstring> name;
    long num;
	*ret = ws_get_connections(&num, &name);

    if(WS_OK == *ret)
    {
        PyObject* py_list = PyList_New(0);
        for(int k = 0; k < name.size(); k++)
        {
            PyList_Append(py_list, Py_BuildValue("u", name[k].data()));
        }
        return py_list;
    }
    else
    {
        return nullptr;
    }
}


//==============================================================================
/*!
 * @brief reports whether the operating system supports connection sharing.
 *
 * @param flg: store the flag that supporing connection-sharing or not
 * @return
 * @retval
 */
//==============================================================================
WS_API int WS_CALL ws_support_connection_sharing(bool* flg)
{
    // 初始化COM库以供调用线程使用
    CoInitialize(NULL);

    // init security to enum RAS connections
    CoInitializeSecurity(NULL, -1, NULL, NULL,
                        RPC_C_AUTHN_LEVEL_PKT,
                        RPC_C_IMP_LEVEL_IMPERSONATE,
                        NULL, EOAC_NONE, NULL);

    // INetSharingManager: Primary interface for Manager object
    INetSharingManager* pNSM = NULL;

    // 用指定的类标识符创建一个Com对象
    HRESULT hr = ::CoCreateInstance(__uuidof(NetSharingManager),
                        NULL,
                        CLSCTX_ALL,
                        __uuidof(INetSharingManager),
                        (void**)&pNSM);
    if (!pNSM)
    {
        CoUninitialize();
        return WS_ERR_CREATE;
    }
    else
    {
        VARIANT_BOOL tmp;
        hr = pNSM->get_SharingInstalled(&tmp);
        *flg = (tmp == -1) ? true : false;
    }

    CoUninitialize();
    return WS_OK;
}


