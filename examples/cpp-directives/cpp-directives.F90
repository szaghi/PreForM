program cpp_directives
implicit none
real:: x,y,z

#define FIRST
#ifdef FIRST
print*,'Ok, "define" and "ifdef-else" work!'
#else
print*,'No, something is wrong with "define" and "ifdef-else"!'
#endif
#undef FIRST
#ifdef FIRST
print*,'No, something is wrong with "undef" and "ifdef-else"!'
#else
print*,'Ok, "undef" and "ifdef-else" work!'
#endif

#define SECOND
#if defined FIRST || defined SECOND
#define THIRD 11
#if defined SECOND && THIRD >= 10
print*, 'Ok, "if-else" nested and operators ("defined", "||", "&&", ">=",etc) work!'
#else
print*,'No, something is wrong with "if-else" nested and operators ("defined", "||", "&&", ">=",etc)!'
#endif
#endif

#define FOURTH
#undef FOURTH
#ifndef FOURTH
print*,'Ok, "ifndef-else" works!'
#else
print*,'No, something is wrong with "ifndef-else"!'
#endif

#ifdef FIRST
print*, 'No, something is wrong with "ifdef"!'
#elif defined THIRD
print*,'Ok, "elif" works!'
#endif

print*,'The macro Third is set to 11 and PreForM expands it to "',THIRD,'". Is it ok?'
print*,'The predefined macros are:'
print*,'  Current file name: __FILE__'
print*,'  Current line number: __LINE__'
print*,'  Current date: __DATE__'
print*,'  Current time: __TIME__'

#include "foo.inc"

#define COMPLEX_EXPR print*,'Ok, the complex expression substitution works!' ; print*,' If you see me it really works!'
COMPLEX_EXPR

#define MYPRINT(x) print*,'Ok ',x,' works!'
MYPRINT('simple function-like macros')
#define FRAC(a,b) a/b
y = 1.
z = 2.
x = FRAC(y,z)
print*,'x = ',x,' if it is 0.5 complex function-like macros work!'

#define MYWARN(COND) if (COND) print*,'Ok, stringification of '//#COND//' works!'
MYWARN(x<2.0)

#define MYCONCAT(x) print*,'Ok, x ## -operator works!'
MYCONCAT(concatenation)

#define VARIADIC_MACRO(...) print*,'Ok,',#__VA_ARGS__,' works also within stringification operator!'
VARIADIC_MACRO( variadic ,macro)
endprogram cpp_directives
