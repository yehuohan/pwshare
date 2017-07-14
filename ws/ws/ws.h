
//==============================================================================
/*!
 * @file ws.h
 * @brief wifi-share dll
 *
 * used to manage starting and closing network connection-sharing.
 *
 * @date
 * @version
 * @author yehuohan, yehuohan@qq.com, yehuohan@gmail.com
 * @copyright
 */
//==============================================================================

#ifndef _WS_H
#define _WS_H


//==============================================================================
/* Include */

#include <stdio.h>
#include <iostream>
#include <vector>

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <objbase.h>
#include <netcon.h>
#include <Wlanapi.h>
#pragma comment(lib, "ole32.lib")
#pragma comment(lib, "oleaut32.lib")
#pragma comment(lib, "Wlanapi.lib")

#include <Python.h>

/* Include End */
//==============================================================================


//==============================================================================
/* Macro */

//#define WS_API
#ifndef WS_API

#define WS_API_EXPORT		__declspec(dllexport)
#define WS_MAPI_IMPORT		__declspec(dllimport)
#define WS_CALL				__stdcall

// build dll
#define __BUILD_DLL
#ifdef __BUILD_DLL
#define WS_API	WS_API_EXPORT 
#else
#define WS_API	WS_API_IMPORT
#endif

#endif
/*! @} */


/*!
 * @addtogroup WS_API
 * 
 * @{
 */

/*!
 * @name return value of funtion
 * @{
 */
#define WS_OK                   0x00        /**< function is executed successfule */
#define WS_ERR_CREATE           0x01        /**< error when creating NetSharingManager instance */
#define WS_ERR_SHARE_EN_HN      0x02        /**< error when enable sharing hostednetwork */
#define WS_ERR_SHARE_EN_ETH     0x03        /**< error when enable sharing ethernet */
#define WS_ERR_SHARE_DIS        0x04        /**< error when disable sharing connection */
#define WS_ERR_GET_CONNECTION   0x05        /**< error when getting information of connections */
/*! @} */
/*! @} */


/* Macro End */
//==============================================================================


//==============================================================================
/* Function */

#ifdef __cplusplus
extern "C"{
#endif


/*!
 * @defgroup WS_API ws dll module
 * 
 * 用于实现wifi连接共享，基于Windows系统API而实现。
 * 最后使用python调用dll库中的接口函数。
 *
 * @{
 */

/*!
 * @name interface of ws dll
 * @{
 */
	WS_API int WS_CALL ws_enable_sharing(const wchar_t* eth_name);
    WS_API int WS_CALL ws_disable_sharing(const wchar_t* eth_name);
	WS_API int WS_CALL ws_get_connections(long* num, std::vector<std::wstring>* name);
    WS_API int WS_CALL ws_support_connection_sharing(bool* flg);

	WS_API PyObject* WS_CALL ws_py_get_connections(int* ret);
/*! @} */
/*! @} */

    // WS_API int WS_CALL ws_set_hostednetwork(const wchar_t* ssid, const wchar_t* key);
    // WS_API int WS_CALL ws_start_hostednetwork();
    // WS_API int WS_CALL ws_stop_hostednetwork();
    // WS_API int WS_CALL ws_close_hostednetwork();
    // WS_API int WS_CALL ws_show_hostednetwork();

#ifdef __cplusplus
}
#endif

/* Function End */
//==============================================================================

#endif	// _WS_H
