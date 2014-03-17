
c  -------------------------------------------------------------------
c            PVM 3.2:  Parallel Virtual Machine System 3.2
c                University of Tennessee, Knoxville TN.
c            Oak Ridge National Laboratory, Oak Ridge TN.
c                    Emory University, Atlanta GA.
c       Authors:  A. L. Beguelin, J. J. Dongarra, G. A. Geist,
c     W. C. Jiang, R. J. Manchek, B. K. Moore, and V. S. Sunderam
c                    (C) 1992 All Rights Reserved
c 
c                               NOTICE
c 
c  Permission to use, copy, modify, and distribute this software and
c  its documentation for any purpose and without fee is hereby granted
c  provided that the above copyright notice appear in all copies and
c  that both the copyright notice and this permission notice appear in
c  supporting documentation.
c 
c  Neither the Institutions (Emory University, Oak Ridge National
c  Laboratory, and University of Tennessee) nor the Authors make any
c  representations about the suitability of this software for any
c  purpose.  This software is provided ``as is'' without express or
c  implied warranty.
c 
c  PVM 3.2 was funded in part by the U.S. Department of Energy, the
c  National Science Foundation and the State of Tennessee.
c  -------------------------------------------------------------------

c     ----------------------------------
c 	  fpvm3.h
c
c     Definitions to be included with
c     User's Fortran application
c     ----------------------------------

      integer PVMHOST, PVMARCH, PVMDEBUG, PVMTRACE
      integer PVMDEFAULT, PVMRAW, PVMINPLACE
      integer PVMTASKEXIT, PVMHOSTDELETE, PVMHOSTADD
      integer PVMROUTE, PVMDEBUGMASK, PVMAUTOERR
      integer PVMOUTPUTTID, PVMOUTPUTCODE
      integer PVMTRACETID, PVMTRACECODE, PVMFRAGSIZE
      integer PVMDONTROUTE, PVMALLOWDIRECT, PVMROUTEDIRECT
      integer STRING, BYTE1, INTEGER2, INTEGER4
      integer REAL4, COMPLEX8, REAL8, COMPLEX16

      integer PvmOk, PvmSysErr, PvmBadParam, PvmMismatch
      integer PvmNoData, PvmNoHost, PvmNoFile, PvmNoMem
      integer PvmBadMsg, PvmNoBuf, PvmNoSuchBuf
      integer PvmNullGroup, PvmDupGroup, PvmNoGroup
      integer PvmNotInGroup, PvmNoinst, PvmHostFail, PvmNoParent
      integer PvmNotImpl, PvmDSysErr, PvmBadVersion, PvmOutOfRes
      integer PvmDupHost, PvmCantStart, PvmAlready, PvmNoTask
      integer PvmNoEntry, PvmDupEntry

c     --------------------
c     spawn 'flag' options
c     --------------------
      parameter( PVMHOST  =  1)
      parameter( PVMARCH  =  2)
      parameter( PVMDEBUG =  4)
      parameter( PVMTRACE =  8)

c     -------------------------
c     buffer 'encoding' options
c     -------------------------
      parameter( PVMDEFAULT = 0)
      parameter( PVMRAW     = 1)
      parameter( PVMINPLACE = 2)

c     ----------------------
c     notify 'about' options
c     ----------------------
      parameter( PVMTASKEXIT   = 1 )
      parameter( PVMHOSTDELETE = 2 )
      parameter( PVMHOSTADD    = 3 )

c     --------------------------------
c     packing/unpacking 'what' options
c     --------------------------------
      parameter( STRING   = 0)
      parameter( BYTE1    = 1)
      parameter( INTEGER2 = 2)
      parameter( INTEGER4 = 3)
      parameter( REAL4    = 4)
      parameter( COMPLEX8 = 5)
      parameter( REAL8    = 6)
      parameter( COMPLEX16= 7)

c     --------------------------------
c     setopt/getopt options for 'what'
c     --------------------------------
      parameter( PVMROUTE      = 1)
      parameter( PVMDEBUGMASK  = 2)
      parameter( PVMAUTOERR    = 3)
      parameter( PVMOUTPUTTID  = 4)
      parameter( PVMOUTPUTCODE = 5)
      parameter( PVMTRACETID   = 6)
      parameter( PVMTRACECODE  = 7)
      parameter( PVMFRAGSIZE   = 8)

c     --------------------------------------------
c     routing options for 'how' in setopt function
c     --------------------------------------------
      parameter( PVMDONTROUTE  = 1)
      parameter( PVMALLOWDIRECT= 2)
      parameter( PVMROUTEDIRECT= 3)

c     --------------------------
c     error 'info' return values
c     --------------------------
      parameter( PvmOk         =   0)
      parameter( PvmBadParam   =  -2)
      parameter( PvmMismatch   =  -3)
      parameter( PvmNoData     =  -5)
      parameter( PvmNoHost     =  -6)
      parameter( PvmNoFile     =  -7)
      parameter( PvmNoMem      = -10)
      parameter( PvmBadMsg     = -12)
      parameter( PvmSysErr     = -14)
      parameter( PvmNoBuf      = -15)
      parameter( PvmNoSuchBuf  = -16)
      parameter( PvmNullGroup  = -17)
      parameter( PvmDupGroup   = -18)
      parameter( PvmNoGroup    = -19)
      parameter( PvmNotInGroup = -20)
      parameter( PvmNoInst     = -21)
      parameter( PvmHostFail   = -22)
      parameter( PvmNoParent   = -23)
      parameter( PvmNotImpl    = -24)
      parameter( PvmDSysErr    = -25)
      parameter( PvmBadVersion = -26)
      parameter( PvmOutOfRes   = -27)
      parameter( PvmDupHost    = -28)
      parameter( PvmCantStart  = -29)
      parameter( PvmAlready    = -30)
      parameter( PvmNoTask     = -31)
      parameter( PvmNoEntry    = -32)
      parameter( PvmDupEntry   = -33)

