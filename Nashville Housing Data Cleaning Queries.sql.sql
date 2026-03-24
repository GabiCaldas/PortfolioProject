-- ============================================================
-- Nashville Housing Data Cleaning Queries
-- Purpose: Clean and standardize raw Nashville housing data
--          stored in PortfolioProject.dbo.NashvilleHousing
-- ============================================================


-- Preview raw data before any transformations
Select *
From PortfolioProject.dbo.NashvilleHousing


-- ============================================================
-- 1. Standardize Date Format
--    The SaleDate column contains datetime values; convert to
--    plain Date type to remove unnecessary time components.
-- ============================================================

-- Preview the converted date alongside the original column
Select SaleDateConverted, CONVERT(Date, SaleDate)
From PortfolioProject.dbo.NashvilleHousing


-- Attempt to update SaleDate in place (may not persist if column
-- type doesn't accept the conversion directly)
UPDATE NashvilleHousing
SET SaleDate = CONVERT(Date, SaleDate)


-- Add a dedicated converted-date column to guarantee the change sticks
ALTER TABLE NashvilleHousing
Add SaleDateUpdated Date;

-- Populate the new column with the converted date values
UPDATE NashvilleHousing
SET SaleDateConverted = CONVERT(Date, SaleDate)


-- ============================================================
-- 2. Populate Property Address Data
--    Some rows are missing a PropertyAddress. Because records
--    with the same ParcelID share the same property, we can
--    fill nulls by joining the table to itself on ParcelID.
-- ============================================================

-- Review all records ordered by ParcelID to spot null addresses
Select *
From PortfolioProject.dbo.NashvilleHousing
--Where PropertyAddress is null
order by ParcelID


-- Identify rows where PropertyAddress is null and show the
-- matching non-null address from a sibling record (same ParcelID,
-- different UniqueID). ISNULL returns the fallback value.
Select a.parcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, ISNULL(a.PropertyAddress, b.PropertyAddress)
From PortfolioProject.dbo.NashvilleHousing a
JOIN PortfolioProject.dbo.NashvilleHousing b
	on a.ParcelID = b.ParcelID
	AND a.[UniqueID ]<>b.[UniqueID ]
Where a.PropertyAddress is null


-- Fill in the missing addresses using the matched sibling value
UPDATE a
SET PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)
From PortfolioProject.dbo.NashvilleHousing a
JOIN PortfolioProject.dbo.NashvilleHousing b
	on a.ParcelID = b.ParcelID
	AND a.[UniqueID ]<>b.[UniqueID ]
Where a.PropertyAddress is null



-- ============================================================
-- 3. Break Out Address into Individual Columns
--    PropertyAddress is stored as "Street, City". Split it
--    into separate columns using SUBSTRING + CHARINDEX.
--    OwnerAddress is stored as "Street, City, State". Split
--    it using PARSENAME after replacing commas with periods.
-- ============================================================

-- Confirm current data before splitting
Select *
From PortfolioProject.dbo.NashvilleHousing
--Where PropertyAddress is null
--order by ParcelID

-- Preview the two parts extracted from PropertyAddress:
--   Part 1: everything before the comma  -> street address
--   Part 2: everything after the comma   -> city name
SELECT
SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)-1) as Address
, SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress)+1 , LEN(PropertyAddress))as Address

From PortfolioProject.dbo.NashvilleHousing

-- Add and populate the street-address portion column
ALTER TABLE NashvilleHousing
Add PropertySplitAddress Nvarchar(255);

UPDATE NashvilleHousing
SET PropertySplitAddress = SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)-1)


-- Add and populate the city portion column
ALTER TABLE NashvilleHousing
Add PropertySplitCity Nvarchar(255);

UPDATE NashvilleHousing
SET PropertySplitCity = SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress)+1 , LEN(PropertyAddress))



-- Verify the new columns were added correctly
Select *
From PortfolioProject.dbo.NashvilleHousing

-- Remove any leftover staging columns from a previous attempt
ALTER TABLE PortfolioProject.dbo.NashvilleHousing
DROP COLUMN PropertySplitAddress1, PropertySplitCity1;


-- Preview OwnerAddress before splitting
Select OwnerAddress
From PortfolioProject.dbo.NashvilleHousing


-- PARSENAME splits on '.'; replace commas with '.' first.
-- Index 3 = street, 2 = city, 1 = state (PARSENAME counts right-to-left)
SELECT
PARSENAME(REPLACE(OwnerAddress, ',', '.'), 3)
,PARSENAME(REPLACE(OwnerAddress, ',', '.'), 2)
,PARSENAME(REPLACE(OwnerAddress, ',', '.'), 1)
From PortfolioProject.dbo.NashvilleHousing


-- Add and populate owner street-address column
ALTER TABLE NashvilleHousing
Add OwnerSplitAddress Nvarchar(255);

UPDATE NashvilleHousing
SET OwnerSplitAddress = PARSENAME(REPLACE(OwnerAddress, ',', '.'), 3)

-- Add and populate owner city column
ALTER TABLE NashvilleHousing
Add OwnerSplitCity Nvarchar(255);

UPDATE NashvilleHousing
SET OwnerSplitCity = PARSENAME(REPLACE(OwnerAddress, ',', '.'), 2)

-- Add and populate owner state column
ALTER TABLE NashvilleHousing
Add OwnerSplitState Nvarchar(255);

UPDATE NashvilleHousing
SET OwnerSplitState = PARSENAME(REPLACE(OwnerAddress, ',', '.'), 1)

-- Verify all new owner address columns are present
Select *
From PortfolioProject.dbo.NashvilleHousing


-- ============================================================
-- 4. Change Y and N to Yes and No in "Sold as Vacant" Field
--    Standardize values so the field contains only 'Yes'/'No'
--    instead of the mix of 'Y', 'N', 'Yes', 'No'.
-- ============================================================

-- Check distinct values and their frequency before the update
Select Distinct(SoldAsVacant), Count(SoldAsVacant)
From PortfolioProject.dbo.NashvilleHousing
Group by SoldAsVacant
Order by 2


-- Preview the CASE transformation without applying it
Select SoldAsVacant
, CASE When SoldAsVacant = 'Y' THEN 'Yes'
		When SoldAsVacant = 'N' THEN 'No'
		ELSE SoldAsVacant  -- leave 'Yes'/'No' unchanged
		END
From PortfolioProject.dbo.NashvilleHousing


-- Apply the transformation: replace Y->Yes, N->No
UPDATE NashvilleHousing
SET SoldAsVacant= CASE When SoldAsVacant = 'Y' THEN 'Yes'
		When SoldAsVacant = 'N' THEN 'No'
		ELSE SoldAsVacant
		END



-- ============================================================
-- 5. Remove Duplicates
--    Use a CTE with ROW_NUMBER partitioned by the natural key
--    (ParcelID, PropertyAddress, SalePrice, SaleDate,
--    LegalReference) to identify exact duplicate rows.
--    Rows where row_num > 1 are duplicates.
-- ============================================================

WITH RowNumCTE AS (
Select *,
	ROW_NUMBER() OVER (
	PARTITION BY PARCELID,
				PropertyAddress,
				SalePrice,
				SaleDate,
				LegalReference
				ORDER BY
					UniqueID  -- keep the lowest UniqueID as the canonical record
					) row_num


From PortfolioProject.dbo.NashvilleHousing
--ORDER BY ParcelID
)

-- Review duplicate rows before deleting (change SELECT to DELETE to remove them)
Select *
From RowNumCTE
Where row_num > 1
--Order By PropertyAddress


-- Confirm overall record count after duplicate removal
Select *
From PortfolioProject.dbo.NashvilleHousing


-- ============================================================
-- 6. Delete Unused Columns
--    Remove columns that are no longer needed after the data
--    has been cleaned and split into more granular fields:
--    - OwnerAddress    -> replaced by OwnerSplitAddress/City/State
--    - TaxDistrict     -> not used in analysis
--    - PropertyAddress -> replaced by PropertySplitAddress/City
--    - SaleDate        -> replaced by SaleDateConverted
-- ============================================================

-- Preview table before column removal
Select*
From PortfolioProject.dbo.NashvilleHousing

-- Drop the raw/redundant columns
ALTER TABLE PortfolioProject.dbo.NashvilleHousing
DROP COLUMN OwnerAddress, TaxDistrict, PropertyAddress, SaleDate
