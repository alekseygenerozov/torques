include /home/aleksey/rebound/src//Makefile.defs

disk: librebound
	@echo ""
	@echo "Compiling problem file ..."
	$(CC) -I/home/aleksey/rebound/src// -Wl,-rpath,./ $(OPT) $(PREDEF) end_disk.c -L. -lrebound $(LIB) -o rebound_disk
	@echo ""
	@echo "REBOUND compiled successfully."

disk_inc: librebound
	@echo ""
	@echo "Compiling problem file ..."
	$(CC) -I/home/aleksey/rebound/src// -Wl,-rpath,./ $(OPT) $(PREDEF) end_disk_inc.c -L. -lrebound $(LIB) -o rebound_disk_inc
	@echo ""
	@echo "REBOUND compiled successfully."


geo: librebound
	@echo ""
	@echo "Compiling problem file ..."
	$(CC) -I/home/aleksey/rebound/src// -Wl,-rpath,./ $(OPT) $(PREDEF) geo.c -L. -lrebound $(LIB) -o geo
	@echo ""
	@echo "REBOUND compiled successfully."

aa: librebound
	@echo ""
	@echo "Compiling problem file ..."
	$(CC) -I/home/aleksey/rebound/src// -Wl,-rpath,./ $(OPT) $(PREDEF) problema.c -L. -lrebound $(LIB) -o rebounda
	@echo ""
	@echo "REBOUND compiled successfully."

bb: librebound
	@echo ""
	@echo "Compiling problem file ..."
	$(CC) -I/home/aleksey/rebound/src// -Wl,-rpath,./ $(OPT) $(PREDEF) problemb.c -L. -lrebound $(LIB) -o reboundb
	@echo ""
	@echo "REBOUND compiled successfully."

all: librebound
	@echo ""
	@echo "Compiling problem file ..."
	$(CC) -I/home/aleksey/rebound/src// -Wl,-rpath,./ $(OPT) $(PREDEF) problem.c -L. -lrebound $(LIB) -o rebound
	@echo ""
	@echo "REBOUND compiled successfully."

librebound: 
	@echo "Compiling shared library librebound.so ..."
	$(MAKE) -C /home/aleksey/rebound/src//
	@-rm -f librebound.so
	@ln -s /home/aleksey/rebound/src//librebound.so .

clean:
	@echo "Cleaning up shared library librebound.so ..."
	@-rm -f librebound.so
	$(MAKE) -C /home/aleksey/rebound/src// clean
	@echo "Cleaning up local directory ..."
	@-rm -vf rebound
