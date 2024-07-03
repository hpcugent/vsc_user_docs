      program slave
c
      implicit double precision (a-h,o-z)
      integer tids(32)
      include 'fpvm3.h'
c
      dimension data(100)
c
c enroll program in pvm
      call pvmfmytid(mytid)
cwrite(*,*) 'mytid',mytid
c
c get my masters' tid
      call pvmfparent(mtid)
cwrite(*,*) 'mtid',mtid
c
c receive data from master
      msgtyp = 1
      call pvmfrecv(mtid,msgtyp,info)
      call pvmfunpack(INTEGER4,nproc,1,1,info)
      call pvmfunpack(INTEGER4,tids,nproc,1,info)
      call pvmfunpack(INTEGER4,n,1,1,info)
      call pvmfunpack(REAL8,data,n,1,info)
cwrite(*,*) 'message received'
cwrite(*,*) 'nproc',nproc     
cwrite(*,*) 'n',n     
cwrite(*,*) 'tids',(tids(i),i=1,nproc)
c
c determine which slave I am
      do i = 1,nproc
        if (tids(i).eq.mytid) me=i
      enddo 
cwrite(*,*) 'me',me,tids(me)
c
c do caalculation
      ip = 100/nproc
      ia = ip*(me-1)+1
      ie = ip*me
      if (me.eq.nproc) ie = 100
cwrite(*,*) me,ip,ia,ie
      sum = 0.0d+00
      do i = ia,ie
        sum = sum + data(i)
      enddo
c
c send result to master
      call pvmfinitsend(PVMDEFAULT,info)
      call pvmfpack(INTEGER4,me,1,1,info)
      call pvmfpack(REAL8,sum,1,1,info)
      msgtype = 2
      call pvmfsend(mtid,msgtype,info)
c
c program finished, leave pvm before exciting
      call flush(6)
      call pvmfexit()
c
      end
