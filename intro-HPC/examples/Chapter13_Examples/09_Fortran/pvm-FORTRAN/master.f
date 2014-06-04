      program master
c
      implicit double precision (a-h,o-z)
      integer tids(32),who
      character slavejob*7
      include 'fpvm3.h'
c
      dimension result(32),data(100)
c
c enroll program in pvm
      call pvmfmytid(mytid)
c
c initiate nproc instances of slave progra
c     print *, 'how many slaves [1-32] ?'
c     read *, nproc
      nproc = 17
      slavejob = 'slave.x'
cprint*, 'spawning...',nproc
      call pvmfspawn(slavejob,PVMDEFAULT,'*', nproc,tids,numt)
cprint*, 'spawningdone...',nproc
cprint*, 'tids',(tids(i),i=1,nproc)
c
c === begin user program ===
      n = 100
      do i = 1,100
        data(i) = dble(i)
      enddo
c
c broadcast to all nodes
      call pvmfinitsend(PVMDEFAULT,ibufid)
      call pvmfpack(INTEGER4,nproc,1,1,info)
      call pvmfpack(INTEGER4,tids,nproc,1,info)
      call pvmfpack(INTEGER4,n,1,1,info)
      call pvmfpack(REAL8,data,n,1,info)
      msgtype = 1
      call pvmfmcast(nproc,tids,msgtype,info)
cprint*, 'mssages send...',info
c
c wait for results from nodes
      msgtype = 2
      do i = 1,nproc
        call pvmfrecv(-1,msgtype,ibufid)
        call pvmfunpack(INTEGER4,who,1,1,info)
        call pvmfunpack(REAL8,result(who),1,1,info)
      enddo
c
c write results
cprint*,(result(i),i=1,nproc)
      sum = 0.0d+00
      do i = 1,nproc
        sum = sum + result(i)
      enddo
      print *, sum
c
c program finished, leave pvm before exciting
      call pvmfexit(info)
c
      end
