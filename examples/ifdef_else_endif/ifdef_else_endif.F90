#define FIRST
program ifdef_else_endif
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
endprogram ifdef_else_endif
