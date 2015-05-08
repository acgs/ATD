__author__ = 'greenpants'


i = u"""
documentclass[a4paper,10pt]{article}
%documentclass[a4paper,10pt]{scrartcl}

usepackage[utf8]{inputenc}

title{CS581 - Final Exam}
author{Victor Szczepanski}
date{}

pdfinfo{%
  /Title    ()
  /Author   ()
  /Creator  ()
  /Producer ()
  /Subject  ()
  /Keywords ()
}

begin{document}
maketitle

section{RANGE: Array index is out of bounds}


  subsection{}% Estimate how hard this bug pattern would be to implement "from scratch" using just the ASM library. Your estimate must be only one of the estimates: easy, moderate, or difficult. Justify your choice with an explanation.
    Implementing this bug pattern in ASM would be difficult. The primary source of difficulty is tracking all integer variables in the current scope, since any of them could be used for the array access (we don't know which one will be used
    until the array access occurs). We would need to simulate any operations on those variables to track their current values at the point where the array is accessed. To make it even more difficult, the value of the variable may depend on the order
    that public methods are called in, which ASM does not support.

  subsection{}% 2. Discuss how important this bug pattern is. Is this pattern something that might really occur on real, industrial projects with enough frequency that it is worth it to check for in FindBugs? Why?
  Array out of bounds errors are important to catch, but since ArrayOutOfBounds is not a common exception to catch (usually developers would catch other errors more relevant to the code being used, like IOError), it has the chance to completely kill
  a running process. Furthermore, since off-by-one errors are common, testing for ArrayOutOfBounds can help find some of these bugs.

  subsection{}% 3. Discuss whether or not good testing practices would expose this bug. If not, explain why not, and if so, explain what type of test would uncover it.
  Good testing would find this bug. Even black-box testing using boundaries could find this. However, black-box testing alone may not find all of them - white-box testing, like all def-use pairs, may be required to find all instances.
  Even with these testing practices, some of these bugs may not be feasible to find or test for.

  subsection{}% 4. Is the FindBugs detection of this bug sound? (E.g., will FindBugs incorrectly warn of the bug in cases where it is not really in existence?) Explain.
  FindBugs' detection is sound. Since FindBugs can determine the value of statically determined variables, if a variable used to access an array is determined to be greater than the (statically determined) length of the array, then it is a bug.

  subsection{}% 5. Is the FindBugs detection of this bug complete? (E.g., will FindBugs incorrectly miss the bug in cases where it is really in existence?) Explain.
  FindBugs' detection is complete only for arrays with statically determined lengths and indexes, for the same reason as in 4.
  However, FindBugs cannot determine lengths or indexes that are determined at runtime, so some ArrayOutOfBounds errors can still occur at runtime.

  subsection{}% 6. Could ESCJava be used to check for the pattern (either with the built-in checks that ESC already has, or with user-supplied annotations)? Explain your answer. Would ESCJava likely do better than FindBugs?
  If the variable to be used as the index is made available to ESCJava, then we can use the @assert annotation to test for this - e.g. @assert i $<$ a.length.
  However, ESCJava will produce a warning for any section that textit{might} result in an ArrayOutOfBounds error, since it cannot determine the value of runtime variables.
  So, ESCJava may find more instances than FindBugs, but some of them may be false positives - ESCJava is not complete for this error.

  subsection{}% 7. Could JML be used to detect a run-time occurrence of the bug? If so, explain how you would do this.
  JML could be used to detect a runtime occurrence, in the same way as ESCJava - by inserting an @assert prior to the array access.



section{HRS: HTTP cookie formed from untrusted input}

subsection{}% Estimate how hard this bug pattern would be to implement "from scratch" using just the ASM library. Your estimate must be only one of the estimates: easy, moderate, or difficult. Justify your choice with an explanation.
    Implementing this bug pattern in ASM would be difficult. To check that the input String to an HTTP cookie is untrusted, we would need to check that the String was not encoded previously (since encoding it using e.g. URLEncoder would make it trusted).
    So, we would need to track the String variable from its initial assignment until it is stored in the cookie and verify if any trusted functions were called on it to make it trusted.

  subsection{}% 2. Discuss how important this bug pattern is. Is this pattern something that might really occur on real, industrial projects with enough frequency that it is worth it to check for in FindBugs? Why?
  This bug is important in industry since it can pose a security risk, but it seems that there are several options that render this bug ineffective - for example, URL encoding the strings in the cookie.
  Nevertheless, if a project were not using any form of HTTP sanitation, this would be an important bug to look for.

  subsection{}% 3. Discuss whether or not good testing practices would expose this bug. If not, explain why not, and if so, explain what type of test would uncover it.
  Good testing practices could expose the bug, but only if some of the provided input includes CRLF - that is, that the tester is aware of the HTTP splitting problem, and tests that the code is not vulnerable to it. Otherwise, even with good
  testing practices, the bug may not be exposed.

  subsection{}% 4. Is the FindBugs detection of this bug sound? (E.g., will FindBugs incorrectly warn of the bug in cases where it is not really in existence?) Explain.
  FindBugs' detection is not sound. Although it is unlikely that a response would be crafted this way, it is possible for the server/application sending the response to include two responses in the same response - that is, a legitimate HTTP splitting
  using CRLF. In this case the input is not necessarily untrusted, but it is bad practice.

  subsection{}% 5. Is the FindBugs detection of this bug complete? (E.g., will FindBugs incorrectly miss the bug in cases where it is really in existence?) Explain.
  FindBugs' detection is not complete. The description of the bug states that if FindBugs does find one, then there are most likely others that it missed.
  This can happen if the HTTP cookie was formed from some values at runtime (e.g. from a web browser taking input from a user), so FindBugs has no information about the input.

  subsection{}% 6. Could ESCJava be used to check for the pattern (either with the built-in checks that ESC already has, or with user-supplied annotations)? Explain your answer. Would ESCJava likely do better than FindBugs?
  ESCJava could be used, but it might been very tricky. Suppose we have a function (like URLEncoder) that we know will produce trusted input. Then we could inject a counter for every time the function is accessed. Then we could use an @ensures to ensure
  that the counter was incremented (though it is possible that the developer simply calls the function but does not use its result. Otherwise, since the input is determined at runtime, we could not determine statically if the input contains a CRLF.

  subsection{}% 7. Could JML be used to detect a run-time occurrence of the bug? If so, explain how you would do this.
  JML could use @requires or @assert to do a 'sanititization' check on some provided input to a function - e.g. if the function takes a String parameter textit{author}, we could write
  begin{verbatim}
@requires
(forall int i; 0 <= i && i < author.length-1; !(author[i] + author[i+1]).equals("rn"))
end{verbatim}

This sort of check would need to be done for each type of sanitization.



section{DL: Synchronization on Boolean}

subsection{}% Estimate how hard this bug pattern would be to implement "from scratch" using just the ASM library. Your estimate must be only one of the estimates: easy, moderate, or difficult. Justify your choice with an explanation.
    Implementing this pattern in ASM would be moderate. We would need to track every boxed constant variable (variable created with a getstatic opcode and its type as one of the boxed constants) to see if it is used in a synchronized. If any are,
    we report a bug.

  subsection{}% 2. Discuss how important this bug pattern is. Is this pattern something that might really occur on real, industrial projects with enough frequency that it is worth it to check for in FindBugs? Why?
  This bug pattern is very important in multi-threaded applications. If this bug is present, it may be very difficult for a developer to discover it since it only manifests at runtime,
  and may not always manifest (e.g. if the unrelated function's execution depends on a variable's value at runtime)

  subsection{}% 3. Discuss whether or not good testing practices would expose this bug. If not, explain why not, and if so, explain what type of test would uncover it.
  Good testing may not expose this bug. Since it is inherently a threading problem, it is possible for the bug to not manifest during testing, especially if the testing is focused on unit testing (and so may not execute the unrelated function).

  It is possible that all-paths testing may uncover this bug, but since threaded applications have so many possible paths, it would be difficult (or time consuming) to find the paths that exhibit this bug.

  subsection{}% 4. Is the FindBugs detection of this bug sound? (E.g., will FindBugs incorrectly warn of the bug in cases where it is not really in existence?) Explain.
  FindBugs is unsound for detecting this bug. While it may be very bad for readability, a developer may intend to synchronize on a boxed constant -
  in which case they intend for all synchronized sections that use that constant to actually synchronize on the same lock.

  subsection{}% 5. Is the FindBugs detection of this bug complete? (E.g., will FindBugs incorrectly miss the bug in cases where it is really in existence?) Explain.
  FindBugs is complete for detecting this bug. Since the bug is simply synchronizing on a boxed constant, FindBugs can examine the type of all objects that are synchronized on and determine if any of them are boxed constants.
  If there are, it reports a bug. If they are not, it does not report a bug.

  subsection{}% 6. Could ESCJava be used to check for the pattern (either with the built-in checks that ESC already has, or with user-supplied annotations)? Explain your answer. Would ESCJava likely do better than FindBugs?
  ESCJava could be used to check for the pattern as long as the object to be synchronized on is a variable. If the developer uses a boxed constant directly (e.g. synchronized(Boolean.FALSE){ ... }), ESCJava could not detect it.
  If it is a variable, before the synchronized section the developer could make an assert like: //@ assert lock1 != Boolean.FALSE && lock1 != Boolean.TRUE && ...

  If the variable is a field, then an @ensures or @requires could be used instead of the @assert.

  subsection{}% 7. Could JML be used to detect a run-time occurrence of the bug? If so, explain how you would do this.
  As with ESCJava, an assert in JML can be written before the synchronized section to assert that the lock variable is not one of the boxed constants.


section{DMI: Random object created and used only once}
subsection{}% Estimate how hard this bug pattern would be to implement "from scratch" using just the ASM library. Your estimate must be only one of the estimates: easy, moderate, or difficult. Justify your choice with an explanation.
    Implementing this pattern in ASM would be easy. Since we only need to track the uses of the Random object, we can step through each method's instructions and track when a new Random object is created. Then, we count how many times that object
    is used in an assignment (e.g. by counting how many times the nextInt method is called). At the end of the analysis, we can output warnings for any Random object with a count $<$ 2. Fields work similarly.

  subsection{}% 2. Discuss how important this bug pattern is. Is this pattern something that might really occur on real, industrial projects with enough frequency that it is worth it to check for in FindBugs? Why?
  This kind of bug may be innocuous for many projects where security is not an issue. In industrial projects, the developers should probably use a more robust random number generator,
  but if they will use java.util.Random, then they should use FindBugs to check for it.

  subsection{}% 3. Discuss whether or not good testing practices would expose this bug. If not, explain why not, and if so, explain what type of test would uncover it.
  Good testing would likely not expose this bug, because it is not exactly a bug that could affect the correctness of the software - it will still generate a random number.
  The tester may try to write a test as if it were an attacker, but this is not standard unit testing practice.

  subsection{}% 4. Is the FindBugs detection of this bug sound? (E.g., will FindBugs incorrectly warn of the bug in cases where it is not really in existence?) Explain.
  FindBugs' detection is sound. If it finds a pattern where a Random object is used and then discarded (set to null, out of scope, etc), then there is no other place where that random object is accessed.

  subsection{}% 5. Is the FindBugs detection of this bug complete? (E.g., will FindBugs incorrectly miss the bug in cases where it is really in existence?) Explain.
  FindBugs' detection is not complete. The creation of a new Random object (or its destruction) may be controlled by a runtime variable, so it would be impossible for static analysis to determine if the object was only used once.

  It should be noted that I ran some example code for this in FindBugs, but it did not report any bugs. The following code should produce a bug, but FindBugs does not find it:
  begin{verbatim}
   public void f2(){
        int x = new Random().nextInt(20);
        System.out.println(x);
   }
  end{verbatim}


  subsection{}% 6. Could ESCJava be used to check for the pattern (either with the built-in checks that ESC already has, or with user-supplied annotations)? Explain your answer. Would ESCJava likely do better than FindBugs?
  ESCJava could not check for this pattern without the developer creating an extra variable that counts the number of accesses to each Random object during its lifetime, and asserts that, if it is destroyed, that its count is greater than one.

  However, without doing this extra work, ESCJava has no way to count accesses to objects, nor to tell if an object was destroyed (and especially not local objects).

  subsection{}% 7. Could JML be used to detect a run-time occurrence of the bug? If so, explain how you would do this.
  As with ESCJava, JML could not detect run-time occurrences of this bug since the language does not support counting accesses to an object, or determining if it has been destroyed and reassigned.

end{document}

"""

print len(i.split())/28.0

