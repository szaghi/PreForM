#define FIRST
program cpp_directives

#ifdef FIRST
print*,'Ok, "define" and "ifdef-else" work!'
call first
#else
call second
#endif
#undef FIRST
#ifdef FIRST
call first
#else
print*,'Ok, "undef" works!'
call second
#endif

#define SECOND
#if defined FIRST || defined SECOND
#define THIRD 11
#if defined SECOND && THIRD >= 10
print*, 'Ok, operators work'
call third
#endif
#endif

#ifdef FOURTH
print*, 'No, somethings wrong with "ifdef"!'
#endif
#define FOURTH
#undef FOURTH
#ifndef FOURTH
print*,'Ok, "ifndef-else" works!'
call fourth
#endif

#ifdef FIRST
print*, 'No, somethings wrong with "ifdef"!'
#elif defined THIRD
print*,'Ok, "elif" works!'
print*,'The macro Third is set to 11 and PreForM expands to "',THIRD,'" is ok?'
print*,'The predefined macros are:'
print*,'  Current file name: __FILE__'
print*,'  Current line number: __LINE__'
print*,'  Current date: __DATE__'
print*,'  Current time: __TIME__'
#endif

#include "foo.F90"

contains
  subroutine first
    print*,'I am the First!'
    return
  endsubroutine first
  subroutine second
    print*,'I am the Second!'
    return
  endsubroutine second
  subroutine third
    print*,'I am the Third!'
    return
  endsubroutine third
  subroutine fourth
    print*,'I am the Fourth'
    return
  endsubroutine fourth
endprogram cpp_directives
