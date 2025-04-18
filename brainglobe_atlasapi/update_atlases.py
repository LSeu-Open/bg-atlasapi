import shutil

from rich import print as rprint

from brainglobe_atlasapi.bg_atlas import (
    BrainGlobeAtlas,
    _version_str_from_tuple,
)
from brainglobe_atlasapi.list_atlases import get_downloaded_atlases


def update_atlas(atlas_name, force=False, fn_update=None):
    """Updates a brainglobe_atlasapi atlas from the latest
    available version online.

    Arguments:
    ----------
    atlas_name: str
        Name of the atlas to update.
    force: bool
        If False it checks if the atlas is already at the latest version
        and doesn't update if that's the case.
    fn_update : Callable, Optional
        A callback function to update progress during download.
    """

    atlas = BrainGlobeAtlas(
        atlas_name=atlas_name, check_latest=False, fn_update=fn_update
    )

    # Check if we need to update
    if not force:
        if atlas.check_latest_version(print_warning=False):
            rprint(
                f"[b][magenta2]brainglobe_atlasapi: {atlas.atlas_name} "
                "is already updated "
                f"(version: {_version_str_from_tuple(atlas.local_version)})"
                "[/b]"
            )
            return

    # Delete atlas folder
    rprint(
        "[b][magenta2]brainglobe_atlasapi: "
        f"updating {atlas.atlas_name}[/magenta2][/b]"
    )
    fld = atlas.brainglobe_dir / atlas.local_full_name
    shutil.rmtree(fld)
    if fld.exists():
        raise ValueError(
            "Something went wrong while trying to delete the old version "
            "of the atlas, aborting."
        )

    # Download again
    atlas.download_extract_file()

    # Check that everything went well
    rprint(
        "[b][magenta2]brainglobe_atlasapi: "
        f"{atlas.atlas_name} updated to version: "
        f"{_version_str_from_tuple(atlas.remote_version)}[/magenta2][/b]"
    )


def install_atlas(atlas_name, fn_update=None):
    """Installs a BrainGlobe atlas from the latest
    available version online.

    Arguments
    ---------
    atlas_name : str
        Name of the atlas to update.
    fn_update : Callable, Optional
        A callback function to update progress during download.
    """

    # Check input:
    if not isinstance(atlas_name, str):
        raise TypeError(
            f"Atlas name should be a string, not a "
            f"{type(atlas_name).__name__}."
        )

    # Check if already downloaded:
    available_atlases = get_downloaded_atlases()
    if atlas_name in available_atlases:
        rprint(
            f"[b][magenta2]brainglobe_atlasapi: installing {atlas_name}: "
            "atlas already installed![/magenta2][/b]"
        )
        return

    # Istantiate to download:
    BrainGlobeAtlas(atlas_name, fn_update=fn_update)
