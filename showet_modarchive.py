# Documentation: ModArchive.org Integration
# Source: /home/rizzo/.openclaw/workspace/projects/showet/modarchive_integration.py

class Config:
    """Configuration wrapper for modarchive_integration module."""
    def __init__(self):
        from modarchive_integration import ModArchiveAPI
        self.api = ModArchiveAPI

def main():
    """Entry point for showet-modarchive CLI command."""
    import sys
    from modarchive_integration import ModArchiveAPI
    from pathlib import Path
    
    if len(sys.argv) < 2:
        print("Usage: showet-modarchive [search|download|scan] [options]")
        print("\nCommands:")
        print("  search <query>     Search modules by keyword")
        print("  download <id>      Download module by ID")
        print("  scan <path>        Find modules in demo directory")
        print("\nExamples:")
        print("  showet-modarchive search 'future crew'")
        print("  showet-modarchive download 12345")
        sys.exit(1)
    
    api = ModArchiveAPI()
    command = sys.argv[1]
    
    if command == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        modules = api.search_modules(query)
        print(f"Found {len(modules)} modules:")
        for m in modules[:10]:
            print(
                f"  [{m['id']}] {m['title']} by {m['artist']} ({m['format']})"
            )
    
    elif command == "download":
        if len(sys.argv) < 3:
            print("Error: Module ID required")
            sys.exit(1)
        module_id = int(sys.argv[2])
        path = api.download_module(module_id)
        if path:
            print(f"Module downloaded to: {path}")
    
    elif command == "scan":
        if len(sys.argv) < 3:
            print("Error: Directory path required")
            sys.exit(1)
        demo_path = Path(sys.argv[2])
        modules = api.get_modules_for_demo(demo_path)
        print(f"Found {len(modules)} modules in {demo_path}:")
        for m in modules:
            print(f"  {m.name}")


if __name__ == "__main__":
    main()